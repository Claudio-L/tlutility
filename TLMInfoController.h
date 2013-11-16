//
//  TLMInfoController.h
//  TeX Live Utility
//
//  Created by Adam Maxwell on 12/7/08.
/*
 This software is Copyright (c) 2008-2013
 Adam Maxwell. All rights reserved.
 
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 
 - Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.
 
 - Redistributions in binary form must reproduce the above copyright
 notice, this list of conditions and the following disclaimer in
 the documentation and/or other materials provided with the
 distribution.
 
 - Neither the name of Adam Maxwell nor the names of any
 contributors may be used to endorse or promote products derived
 from this software without specific prior written permission.
 
 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#import <Cocoa/Cocoa.h>

@class TLMPackage, FileView, TLMOutlineView;
@protocol TLMInfo;

@interface TLMInfoController : NSWindowController <NSPathCellDelegate> {
@private
    NSTextView          *_textView;
    NSProgressIndicator *_spinner;
    NSTabView           *_tabView;
    NSOperationQueue    *_infoQueue;
    FileView            *_fileView;
    NSArray             *_fileObjects;
    
    TLMOutlineView      *_outlineView;
    NSMutableArray      *_runfiles;
    NSMutableArray      *_sourcefiles;
    NSMutableArray      *_docfiles;
    NSPathCell          *_clickedCell;
}

+ (TLMInfoController *)sharedInstance;
- (void)showInfoForPackage:(id <TLMInfo>)package location:(NSURL *)mirrorURL;
- (void)cancel;

@property (nonatomic, retain) IBOutlet NSTextView *_textView;
@property (nonatomic, retain) IBOutlet NSProgressIndicator *_spinner;
@property (nonatomic, retain) IBOutlet NSTabView *_tabView;
@property (nonatomic, retain) IBOutlet FileView *_fileView;
@property (nonatomic, retain) IBOutlet TLMOutlineView *_outlineView;

@end
