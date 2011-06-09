#!/usr/bin/env python

import sys
import objc
from Foundation import NSBundle, NSURL

sys.stdout.write("%s\n" % (sys.argv))

bundle_path = sys.argv[3]

bundle = NSBundle.bundleWithPath_(bundle_path)
if not bundle:
    sys.stderr.write("Failed to load bundle %s\n" % (bundle_path))

TLMDatabasePackage = objc.lookUpClass("TLMDatabasePackage")
if not TLMDatabasePackage:
    sys.stderr.write("Failed to find class TLMDatabasePackage\n")
    exit(1)

TLMDatabase = objc.lookUpClass("TLMDatabase")
if not TLMDatabase:
    sys.stderr.write("Failed to find class TLMDatabase\n")
    exit(1)

class Package(TLMDatabasePackage):
    """TeX Live Package"""
    _name = None
    _category = None
    _shortdesc = None
    _longdesc = None
    _catalogue = None
    _relocated = 0
    
    _runfiles = []
    _runsize = None
    
    _srcfiles = []
    _srcsize = None
    
    _docfiles = []
    _docsize = None
    
    # maps keys (doc filenames) to maps of attributes (details, language)
    _docfiledata = {}
    
    _executes = []
    _postactions = []
    
    # maps keys (arch name) to lists of files
    _binfiles = {}
    # maps keys (arch name) to integer size
    _binsize = {}
    
    _depends = []
    _revision = None
    
    _cataloguedata = {}
    
    _extradata = {}
    
    def name(self):
        return self._name
        
    def category(self):
        return self._category
        
    def shortDescription(self):
        return self._shortdesc
        
    def longDescription(self):
        return self._longdesc
        
    def catalogue(self):
        return self._catalogue
        
    def relocated(self):
        return self._relocated
        
    def runFiles(self):
        return self._runfiles
        
    def sourceFiles(self):
        return self._srcfiles
        
    def docFiles(self):
        return self._docfiles
        
    def revision(self):
        return self._revision
        
    def add_pair(self, key, value):
        self._extradata[key] = value
        
    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        s = "%s: %s\n  srcsize=%s\n  srcfiles=%s" % (self._name, self._shortdesc, self._srcsize, self._srcfiles)
        s += "\n  binsize = %s\n  binfiles = %s" % (self._binsize, self._binfiles)
        s += "\n  docsize = %s\n  docfiles = %s\n  docfiledata = %s" % (self._docsize, self._docfiles, self._docfiledata)
        s += "\n  runsize = %s\n  runfiles = %s" % (self._runsize, self._runfiles)
        s += "\n  depends = %s" % (self._depends)
        s += "\n  longdesc = %s" % (self._longdesc)
        s += "\n  cataloguedata = %s" % (self._cataloguedata)
        for k in self._extradata:
            s += "\n  %s = %s" % (k, self._extradata[k])
        return s
        
    def insert_in_packages(self, conn):
        c = conn.cursor()
        c.execute("""INSERT into packages values (?,?,?,?,?,?)""", (self._name, self._category, self._revision, self._shortdesc, self._longdesc, self._runfiles))
        conn.commit()

def _attributes_from_line(line):
    # arch=x86_64-darwin size=1
    # details="Package introduction" language="de"
    key = None
    value = None
    chars = []
    quote_count = 0
    attrs = {}
    for c in line:

        if c == "=":
            
            if key == None:
                assert quote_count == 0, "possibly quoted key in line %s" % (line)
                key = "".join(chars)
                chars = []
            else:
                chars.append(c)
        
        elif c == "\"":
            
            quote_count += 1
            
        elif c == " ":
            
            # if quotes are matched, we've reached the end of a key-value pair
            if quote_count % 2 == 0:
                assert key != None, "no key found for %s" % (line)
                assert key not in attrs, "key already assigned for line %s" % (line)
                attrs[key] = "".join(chars)
                
                # reset parser state
                chars = []
                key = None
                quote_count = 0
            else:
                chars.append(c)
                
        else:
            chars.append(c)
    
    assert key != None, "no key found for %s" % (line)
    assert len(chars), "no values found for line %s" % (line)
    attrs[key] = "".join(chars)
    return attrs

def packages_from_tlpdb(flat_tlpdb):
                
    package = None
    package_index = 0
    all_packages = []
    index_map = {}
    last_key = None
    last_arch = None

    for line in flat_tlpdb:
                
        line = line.strip("\r\n")
    
        if len(line) == 0:
            all_packages.append(package)
            index_map[package._name] = package_index
            
            package_index += 1
            package = None
            last_key = None
            last_arch = None
        else:
            
            # the first space token is a delimiter
            key, ignored, value = line.partition(" ")
                            
            if package == None:
                assert key == "name", "first line must be a name"
                package = Package.new()
        
            line_has_key = True
            if len(key) == 0:
                key = last_key
                line_has_key = False
                        
            if key == "name":
                package._name = value
            elif key == "category":
                package._category = value
            elif key == "revision":
                package._revision = int(value)
            elif key == "relocated":
                package._relocated = int(value)
            elif key == "shortdesc":
                package._shortdesc = value.decode("utf-8")
            elif key == "longdesc":
                oldvalue = "" if package._longdesc == None else package._longdesc
                package._longdesc = oldvalue + " " + value.decode("utf-8")
            elif key == "depend":
                package._depends.append(value)
            elif key == "catalogue":
                package._catalogue = value
            elif key.startswith("catalogue-"):
                catkey = key[len("catalogue-"):]
                package._cataloguedata[catkey] = value
            elif key == "srcfiles":
                if line_has_key:
                    attrs = _attributes_from_line(value)
                    assert "size" in attrs, "missing size for %s : %s" % (package._name, key)
                    package._srcsize = int(attrs["size"])
                else:
                    package._srcfiles.append(value)
            elif key == "binfiles":
                if line_has_key:
                    attrs = _attributes_from_line(value)
                    assert "arch" in attrs, "missing arch for %s : %s" % (package._name, key)
                    last_arch = attrs["arch"]
                    assert "size" in attrs, "missing size for %s : %s" % (package._name, key)
                    package._binsize[last_arch] = int(attrs["size"])
                else:
                    oldvalue = package._binfiles[last_arch] if last_arch in package._binfiles else []
                    oldvalue.append(value)
                    package._binfiles[last_arch] = oldvalue
            elif key == "docfiles":
                if line_has_key:
                    attrs = _attributes_from_line(value)
                    assert "size" in attrs, "missing size for %s : %s" % (package._name, key)
                    package._docsize = int(attrs["size"])
                else:
                    values = value.split(" ")
                    if len(values) > 1:
                        package._docfiledata[values[0]] = _attributes_from_line(" ".join(values[1:]))
                    package._docfiles.append(values[0])
            elif key == "runfiles":
                if line_has_key:
                    attrs = _attributes_from_line(value)
                    assert "size" in attrs, "missing size for %s : %s" % (package._name, key)
                    package._runsize = int(attrs["size"])
                else:
                    package._runfiles.append(value)
            elif key == "postaction":
                package._postactions.append(value)
            elif key == "execute":
                package._executes.append(value)
            else:
                package._add_pair(key, value)
                #assert False, "unhandled line %s" % (line)
                
            last_key = key

    return all_packages, index_map
    
def convert_to_sqlite(packages):
    
    import sqlite3

    DB_PATH = "/tmp/texlive.sqlite3"

    def adapt_list(lst):
        return "\0".join(lst) if lst else None

    def convert_list(s):
        return s.split("\0") if s else None

    sqlite3.register_adapter(list, adapt_list)
    sqlite3.register_converter("list", convert_list)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute("""CREATE table packages (name text, category text, revision real, shortdesc text, longdesc text, runfiles list)""")
    
    for pkg in packages:
        pkg.insert_in_packages(conn)
    
    conn.close()  
    
if __name__ == '__main__':
    
    with open(sys.argv[1]) as flat_tlpdb:
        all_packages, index_map = packages_from_tlpdb(flat_tlpdb)

        pkg = all_packages[index_map["00texlive.installation"]]
        for dep in pkg._depends:
            if dep.startswith("opt_"):
                key, ignored, value = dep[4:].partition(":")
                sys.stdout.write("%s = %s\n" % (key, value))

    db = TLMDatabase.alloc().initWithPackages_(all_packages)
    url = NSURL.URLWithString_(sys.argv[2])
    TLMDatabase.addDatabase_forURL_(db, url)  
            
    #exit(0)

    # for idx, pkg in enumerate(all_packages):
    #     
    #     if pkg.name == "achemso":
    #         break
    #     
    #     if idx % 4 == 0 or pkg.name == "a2ping":
    #         print pkg
    #         print ""