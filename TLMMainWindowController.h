//
//  TLMMainWindowController.h
//  TeX Live Manager
//
//  Created by Adam Maxwell on 12/6/08.
/*
 This software is Copyright (c) 2008
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

@class TLMSplitView;
@class TLMLogDataSource;
@class TLMStatusView;
@class TLMPackageListDataSource;
@class TLMUpdateListDataSource;
@class TLMTabView;
@class TLMGradientView;

@interface TLMMainWindowController : NSWindowController 
{
@private
    NSProgressIndicator      *_progressIndicator;
    NSTextField              *_hostnameField;
    TLMTabView               *_tabView;
    TLMSplitView             *_splitView;
    TLMStatusView            *_statusView;
    TLMGradientView          *_statusBarView;
    
    NSOperationQueue         *_queue;
    CGFloat                   _lastTextViewHeight;
    BOOL                      _updateInfrastructure;
    NSURL                    *_lastUpdateURL;
    
    TLMUpdateListDataSource  *_updateListDataSource;
    TLMLogDataSource         *_logDataSource;
    TLMPackageListDataSource *_packageListDataSource;
}

@property (nonatomic, retain) IBOutlet NSProgressIndicator *_progressIndicator;
@property (nonatomic, retain) IBOutlet NSTextField *_hostnameField;
@property (nonatomic, retain) IBOutlet TLMSplitView *_splitView;
@property (nonatomic, retain) IBOutlet TLMStatusView *_statusView;
@property (nonatomic, retain) IBOutlet TLMLogDataSource *_logDataSource;
@property (nonatomic, retain) IBOutlet TLMPackageListDataSource *_packageListDataSource;
@property (nonatomic, retain) IBOutlet TLMUpdateListDataSource *_updateListDataSource;
@property (nonatomic, retain) IBOutlet TLMTabView *_tabView;
@property (nonatomic, retain) IBOutlet TLMGradientView *_statusBarView;
@property (nonatomic, readonly) BOOL infrastructureNeedsUpdate;
@property (nonatomic, copy) NSURL *lastUpdateURL;

- (IBAction)changePapersize:(id)sender;
- (IBAction)cancelAllOperations:(id)sender;

// install/update actions will use -lastUpdateURL
- (void)updateAllPackages;
- (void)installPackagesWithNames:(NSArray *)packageNames reinstall:(BOOL)reinstall;
- (void)updatePackagesWithNames:(NSArray *)packageNames;

- (void)removePackagesWithNames:(NSArray *)packageNames;

// both of these will use the default server URL
- (void)refreshFullPackageList;
- (void)refreshUpdatedPackageList;

@end
