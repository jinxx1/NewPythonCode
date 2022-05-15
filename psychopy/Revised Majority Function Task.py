#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.1.2),
    on 四月 01, 2022, at 02:04
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.1.2'
expName = 'Revised Majority Function Task'  # from the Builder filename that created this script
expInfo = {'language': ['English', 'Chinese'], 'participant': '', 'session': '001', 'task': ['MFT_R', 'MFT_M', 'practice'], 'precision': [None, 0.05, 0.04, 0.03, 0.02, 0.01]}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_Session%s_%s' % (expInfo['task'], expInfo['session'], expInfo['participant'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='D:\\PythonCode\\psychopy\\Revised Majority Function Task.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1536, 864], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# Setup ioHub
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# Initialize components for Routine "welcome"
welcomeClock = core.Clock()
text_welcome = visual.TextStim(win=win, name='text_welcome',
    text='欢迎参加实验',
    font='Arial',
    pos=(0, 0), height=0.07, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
text_MFT = visual.TextStim(win=win, name='text_MFT',
    text='Majority Function Task\n',
    font='Arial',
    pos=(0, 0.3), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
text_indicate = visual.TextStim(win=win, name='text_indicate',
    text='屏幕上会呈现3或5个箭头，这些箭头可能指向左也可能指向右',
    font='Arial',
    pos=(0, 0.22), height=0.04, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
image_instr = visual.ImageStim(
    win=win,
    name='image_instr', 
    image='image/instr.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.02), size=(1.2, 0.4),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
key_welcome = keyboard.Keyboard()
text_target = visual.TextStim(win=win, name='text_target',
    text='你的任务是指出在屏幕上所呈现的箭头中，大多数箭头所指的方向',
    font='Arial',
    pos=(0, -0.2), height=0.04, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-5.0);
text_press = visual.TextStim(win=win, name='text_press',
    text='如果判断多数箭头方向为左请按F键，判断为右请按J键',
    font='Arial',
    pos=(0, -0.32), height=0.04, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-6.0);
text_continue = visual.TextStim(win=win, name='text_continue',
    text='按空格继续...',
    font='Arial',
    pos=(0, -0.42), height=0.05, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-7.0);
# initialize the parameters
if expInfo['task'] == 'MFT_R':
    N = 2
else:
    N = 1
listACC = []
ETs = [0.25, 0.5, 1, 2]
Ratios = ['ratio32', 'ratio41', 'ratio21']
listECCC = []
if expInfo['task'] == 'MFT_M':
    Ratios = ['ratio32', 'ratio41', 'ratio21', 'ratio30', 'ratio50', 'ratio10']

# Initialize components for Routine "initialize"
initializeClock = core.Clock()
ECCC = None
cat = False


# Initialize components for Routine "prep"
prepClock = core.Clock()
fix_prep = visual.ImageStim(
    win=win,
    name='fix_prep', 
    image='image/fix.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
prepare = True

# get a dict of the predicted accuracy
if expInfo['task'] == 'MFT_R':
    with open("dictDeriv.txt", 'r') as fDeriv:
        dictDeriv = eval(fDeriv.read())

# pick the condition according to ECCC
def selection(ECCC):
    c = round(ECCC, 2)
    listDeriv = []
    for i in Ratios:
        for j in ETs:
            deriv = dictDeriv[(c, i, j)]
            listDeriv.append(deriv)
    derivSum = np.sum(listDeriv)
    temp = np.random.uniform(0, derivSum)
    curr_sum = 0
    ret = None
    for n in range(12):
        curr_sum += listDeriv[n]
        if temp <= curr_sum:
            ret = '%s' % n
            break
    return ret

# Initialize components for Routine "trial"
trialClock = core.Clock()
fix_start = visual.ImageStim(
    win=win,
    name='fix_start', 
    image='image/fix.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
mask1 = visual.ImageStim(
    win=win,
    name='mask1', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(0.2, 0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
mask2 = visual.ImageStim(
    win=win,
    name='mask2', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(0.13, 0.13), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
mask3 = visual.ImageStim(
    win=win,
    name='mask3', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(0, 0.2), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
mask4 = visual.ImageStim(
    win=win,
    name='mask4', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(-0.13, 0.13), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
mask5 = visual.ImageStim(
    win=win,
    name='mask5', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(-0.2, 0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
mask6 = visual.ImageStim(
    win=win,
    name='mask6', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(-0.13, -0.13), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
mask7 = visual.ImageStim(
    win=win,
    name='mask7', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(0, -0.2), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)
mask8 = visual.ImageStim(
    win=win,
    name='mask8', 
    image='image/mask.png', mask=None, anchor='center',
    ori=0, pos=(0.13, -0.13), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-8.0)
key_resp = keyboard.Keyboard()
import numpy as np

# change the images according to the amount of arrows(left, right)
def imageSet(leftN, rightN):
    images = [None, None, None, None, None]
    for i in range(leftN):
        images[i] = 'image/left.png'
    for j in range(rightN):
        images[leftN + j] = 'image/right.png'
    return images
image1 = visual.ImageStim(
    win=win,
    name='image1', 
    image=None, mask=None, anchor='center',
    ori=0, pos=(0,0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-11.0)
image2 = visual.ImageStim(
    win=win,
    name='image2', 
    image=None, mask=None, anchor='center',
    ori=0, pos=(0,0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-12.0)
image3 = visual.ImageStim(
    win=win,
    name='image3', 
    image=None, mask=None, anchor='center',
    ori=0, pos=(0,0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-13.0)
image4 = visual.ImageStim(
    win=win,
    name='image4', 
    image=None, mask=None, anchor='center',
    ori=0, pos=(0,0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-14.0)
image5 = visual.ImageStim(
    win=win,
    name='image5', 
    image=None, mask=None, anchor='center',
    ori=0, pos=(0,0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-15.0)

# Initialize components for Routine "feedbacks"
feedbacksClock = core.Clock()
feedback = visual.TextStim(win=win, name='feedback',
    text='正确',
    font='Arial',
    pos=(0, 0), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
fix_end = visual.ImageStim(
    win=win,
    name='fix_end', 
    image='image/fix.png', mask=None, anchor='center',
    ori=0, pos=(0, 0), size=(0.06, 0.06),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Initialize components for Routine "estimation"
estimationClock = core.Clock()
key_rest = keyboard.Keyboard()
text_rest = visual.TextStim(win=win, name='text_rest',
    text='休息片刻，可按空格跳过',
    font='Arial',
    pos=(0, 0), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
import pandas as pd
import csv

# get a dict of the predicted accuracy
with open("dictEACC.txt", 'r') as fEACC:
    dictEACC = eval(fEACC.read())

# ECCC estimation using the accuracy matrix
def getECCC(dfACC):
    #empirical accuracy
    dictACC = {}
    for i in Ratios:
        for j in ETs:
            dfTemp = dfACC[(dfACC.ETs == j) & (dfACC.Ratios == i)]
            acc = dfTemp['ACC'].mean()
            dictACC.update({(i,j):acc})

    # maximun likelihood estimation
    lastL = False
    for c in np.arange(0, 10, 0.01):
        c = round(c, 2)
        lnL = np.log(1)
        for i in Ratios:
            for j in ETs:
                Eacc = dictEACC[(c, i, j)]
                #Eacc = getEacc(c, i, j)
                ACC = dictACC[(i, j)]
                if Eacc == 1:
                    Eacc =0.999
                elif Eacc == 0:
                    Eacc = 0.001
                lnL = lnL + ACC * np.log(Eacc) + (1 - ACC) * np.log(1 - Eacc)
        L = -2*lnL
        if lastL == False:
            lastL = L
            ECCC = c
        elif L < lastL:
            lastL = L
            ECCC = c
    return ECCC

# Initialize components for Routine "end"
endClock = core.Clock()
text_end = visual.TextStim(win=win, name='text_end',
    text='The end',
    font='Arial',
    pos=(0, 0), height=0.08, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_end = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "welcome"-------
continueRoutine = True
# update component parameters for each repeat
key_welcome.keys = []
key_welcome.rt = []
_key_welcome_allKeys = []
if expInfo['language'] == 'English':
    msg0 = 'welcome to the experiment'
    msg1 = "Several arrows would be shown on the screen pointing left or right, for example:"
    msg2 = 'Your task is to indicate the direction in which the majority of the arrows point.'
    msg3 = "Press the 'F' button if the direction was left, or the 'J' button if the direction was right."
    msg4 = 'Press space bar to continue...'
    text_welcome.setText(msg0)
    text_indicate.setText(msg1)
    text_target.setText(msg2)
    text_press.setText(msg3)
    text_continue.setText(msg4)
# keep track of which components have finished
welcomeComponents = [text_welcome, text_MFT, text_indicate, image_instr, key_welcome, text_target, text_press, text_continue]
for thisComponent in welcomeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
welcomeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "welcome"-------
while continueRoutine:
    # get current time
    t = welcomeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=welcomeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_welcome* updates
    if text_welcome.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_welcome.frameNStart = frameN  # exact frame index
        text_welcome.tStart = t  # local t and not account for scr refresh
        text_welcome.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_welcome, 'tStartRefresh')  # time at next scr refresh
        text_welcome.setAutoDraw(True)
    if text_welcome.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text_welcome.tStartRefresh + 1-frameTolerance:
            # keep track of stop time/frame for later
            text_welcome.tStop = t  # not accounting for scr refresh
            text_welcome.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text_welcome, 'tStopRefresh')  # time at next scr refresh
            text_welcome.setAutoDraw(False)
    
    # *text_MFT* updates
    if text_MFT.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        text_MFT.frameNStart = frameN  # exact frame index
        text_MFT.tStart = t  # local t and not account for scr refresh
        text_MFT.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_MFT, 'tStartRefresh')  # time at next scr refresh
        text_MFT.setAutoDraw(True)
    
    # *text_indicate* updates
    if text_indicate.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        text_indicate.frameNStart = frameN  # exact frame index
        text_indicate.tStart = t  # local t and not account for scr refresh
        text_indicate.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_indicate, 'tStartRefresh')  # time at next scr refresh
        text_indicate.setAutoDraw(True)
    
    # *image_instr* updates
    if image_instr.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        image_instr.frameNStart = frameN  # exact frame index
        image_instr.tStart = t  # local t and not account for scr refresh
        image_instr.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(image_instr, 'tStartRefresh')  # time at next scr refresh
        image_instr.setAutoDraw(True)
    
    # *key_welcome* updates
    waitOnFlip = False
    if key_welcome.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
        # keep track of start time/frame for later
        key_welcome.frameNStart = frameN  # exact frame index
        key_welcome.tStart = t  # local t and not account for scr refresh
        key_welcome.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_welcome, 'tStartRefresh')  # time at next scr refresh
        key_welcome.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_welcome.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_welcome.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_welcome.status == STARTED and not waitOnFlip:
        theseKeys = key_welcome.getKeys(keyList=['space'], waitRelease=False)
        _key_welcome_allKeys.extend(theseKeys)
        if len(_key_welcome_allKeys):
            key_welcome.keys = _key_welcome_allKeys[-1].name  # just the last key pressed
            key_welcome.rt = _key_welcome_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # *text_target* updates
    if text_target.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        text_target.frameNStart = frameN  # exact frame index
        text_target.tStart = t  # local t and not account for scr refresh
        text_target.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_target, 'tStartRefresh')  # time at next scr refresh
        text_target.setAutoDraw(True)
    
    # *text_press* updates
    if text_press.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        text_press.frameNStart = frameN  # exact frame index
        text_press.tStart = t  # local t and not account for scr refresh
        text_press.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_press, 'tStartRefresh')  # time at next scr refresh
        text_press.setAutoDraw(True)
    
    # *text_continue* updates
    if text_continue.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        text_continue.frameNStart = frameN  # exact frame index
        text_continue.tStart = t  # local t and not account for scr refresh
        text_continue.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_continue, 'tStartRefresh')  # time at next scr refresh
        text_continue.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in welcomeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "welcome"-------
for thisComponent in welcomeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "welcome" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
MFTR = data.TrialHandler(nReps=N, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='MFTR')
thisExp.addLoop(MFTR)  # add the loop to the experiment
thisMFTR = MFTR.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisMFTR.rgb)
if thisMFTR != None:
    for paramName in thisMFTR:
        exec('{} = thisMFTR[paramName]'.format(paramName))

for thisMFTR in MFTR:
    currentLoop = MFTR
    # abbreviate parameter names if possible (e.g. rgb = thisMFTR.rgb)
    if thisMFTR != None:
        for paramName in thisMFTR:
            exec('{} = thisMFTR[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "initialize"-------
    continueRoutine = True
    # update component parameters for each repeat
    # initialize the parameters
    if expInfo['task'] == 'MFT_M':
        blockN = 1
        blockCondition = 'conditions/MFT_M_blocks.xlsx'
    else:
        blockCondition = 'conditions/MFT_R_blocks.xlsx'
        if expInfo['task'] == 'practice':
            blockN = 8
        elif expInfo['task'] == 'MFT_R' and cat == False:
            blockN = 1
        else:
            blockN = 192
    # keep track of which components have finished
    initializeComponents = []
    for thisComponent in initializeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    initializeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "initialize"-------
    while continueRoutine:
        # get current time
        t = initializeClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=initializeClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in initializeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "initialize"-------
    for thisComponent in initializeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "initialize" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    blocks = data.TrialHandler(nReps=blockN, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(blockCondition),
        seed=None, name='blocks')
    thisExp.addLoop(blocks)  # add the loop to the experiment
    thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    for thisBlock in blocks:
        currentLoop = blocks
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock:
                exec('{} = thisBlock[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "prep"-------
        continueRoutine = True
        # update component parameters for each repeat
        if prepare == True:
            prepTime = 2
        else:
            prepTime = 0
        # keep track of which components have finished
        prepComponents = [fix_prep]
        for thisComponent in prepComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        prepClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "prep"-------
        while continueRoutine:
            # get current time
            t = prepClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=prepClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix_prep* updates
            if fix_prep.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                fix_prep.frameNStart = frameN  # exact frame index
                fix_prep.tStart = t  # local t and not account for scr refresh
                fix_prep.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix_prep, 'tStartRefresh')  # time at next scr refresh
                fix_prep.setAutoDraw(True)
            if fix_prep.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix_prep.tStartRefresh + prepTime-frameTolerance:
                    # keep track of stop time/frame for later
                    fix_prep.tStop = t  # not accounting for scr refresh
                    fix_prep.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(fix_prep, 'tStopRefresh')  # time at next scr refresh
                    fix_prep.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in prepComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "prep"-------
        for thisComponent in prepComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # initialize the parameters
        if expInfo['task'] == 'MFT_M':
            repN = 1
            pick = ':'
        elif expInfo['task'] == 'practice':
            repN = 1
            pick = ':'
        elif expInfo['task'] == 'MFT_R' and cat == False:
            repN = 2
            pick = ':'
            prepare = False
        else:
            repN = 1
            prepare = False
            pick = selection(ECCC)
        # the Routine "prep" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler(nReps=repN, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions(trailCondition, selection=pick),
            seed=None, name='trials')
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        for thisTrial in trials:
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            continueRoutine = True
            # update component parameters for each repeat
            key_resp.keys = []
            key_resp.rt = []
            _key_resp_allKeys = []
            # randomnize the correctAns
            correctRand = np.random.randint(2)
            if correctRand == 1:
                correctAns = 'f'
            else:
                correctAns = 'j'
            
            trials.addData('pickIndex',pick)
            trials.addData('correctAns.keys',correctAns)
            
            
            # set the images according to the ratio of the trial
            majorN, minorN = int(Ratio[5]), int(Ratio[6])
            if correctAns == 'f':
                images = imageSet(majorN, minorN)
            else:
                images = imageSet(minorN, majorN)
            image1.setImage(images[0])
            image2.setImage(images[1])
            image3.setImage(images[2])
            image4.setImage(images[3])
            image5.setImage(images[4])
            
            
            
            # shuffle the positions
            positions = [(0.2, 0), (0.13, 0.13), (0, 0.2), (-0.13, 0.13), (-0.2, 0), (-0.13, -0.13), (0, -0.2), (0.13, -0.13)].copy()
            np.random.shuffle(positions)
            image1.setPos(positions[0])
            image2.setPos(positions[1])
            image3.setPos(positions[2])
            image4.setPos(positions[3])
            image5.setPos(positions[4])
            
            
            # keep track of which components have finished
            trialComponents = [fix_start, mask1, mask2, mask3, mask4, mask5, mask6, mask7, mask8, key_resp, image1, image2, image3, image4, image5]
            for thisComponent in trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "trial"-------
            while continueRoutine:
                # get current time
                t = trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *fix_start* updates
                if fix_start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    fix_start.frameNStart = frameN  # exact frame index
                    fix_start.tStart = t  # local t and not account for scr refresh
                    fix_start.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fix_start, 'tStartRefresh')  # time at next scr refresh
                    fix_start.setAutoDraw(True)
                if fix_start.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > fix_start.tStartRefresh + 3-frameTolerance:
                        # keep track of stop time/frame for later
                        fix_start.tStop = t  # not accounting for scr refresh
                        fix_start.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(fix_start, 'tStopRefresh')  # time at next scr refresh
                        fix_start.setAutoDraw(False)
                
                # *mask1* updates
                if mask1.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask1.frameNStart = frameN  # exact frame index
                    mask1.tStart = t  # local t and not account for scr refresh
                    mask1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask1, 'tStartRefresh')  # time at next scr refresh
                    mask1.setAutoDraw(True)
                if mask1.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask1.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask1.tStop = t  # not accounting for scr refresh
                        mask1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask1, 'tStopRefresh')  # time at next scr refresh
                        mask1.setAutoDraw(False)
                
                # *mask2* updates
                if mask2.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask2.frameNStart = frameN  # exact frame index
                    mask2.tStart = t  # local t and not account for scr refresh
                    mask2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask2, 'tStartRefresh')  # time at next scr refresh
                    mask2.setAutoDraw(True)
                if mask2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask2.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask2.tStop = t  # not accounting for scr refresh
                        mask2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask2, 'tStopRefresh')  # time at next scr refresh
                        mask2.setAutoDraw(False)
                
                # *mask3* updates
                if mask3.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask3.frameNStart = frameN  # exact frame index
                    mask3.tStart = t  # local t and not account for scr refresh
                    mask3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask3, 'tStartRefresh')  # time at next scr refresh
                    mask3.setAutoDraw(True)
                if mask3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask3.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask3.tStop = t  # not accounting for scr refresh
                        mask3.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask3, 'tStopRefresh')  # time at next scr refresh
                        mask3.setAutoDraw(False)
                
                # *mask4* updates
                if mask4.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask4.frameNStart = frameN  # exact frame index
                    mask4.tStart = t  # local t and not account for scr refresh
                    mask4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask4, 'tStartRefresh')  # time at next scr refresh
                    mask4.setAutoDraw(True)
                if mask4.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask4.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask4.tStop = t  # not accounting for scr refresh
                        mask4.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask4, 'tStopRefresh')  # time at next scr refresh
                        mask4.setAutoDraw(False)
                
                # *mask5* updates
                if mask5.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask5.frameNStart = frameN  # exact frame index
                    mask5.tStart = t  # local t and not account for scr refresh
                    mask5.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask5, 'tStartRefresh')  # time at next scr refresh
                    mask5.setAutoDraw(True)
                if mask5.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask5.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask5.tStop = t  # not accounting for scr refresh
                        mask5.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask5, 'tStopRefresh')  # time at next scr refresh
                        mask5.setAutoDraw(False)
                
                # *mask6* updates
                if mask6.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask6.frameNStart = frameN  # exact frame index
                    mask6.tStart = t  # local t and not account for scr refresh
                    mask6.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask6, 'tStartRefresh')  # time at next scr refresh
                    mask6.setAutoDraw(True)
                if mask6.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask6.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask6.tStop = t  # not accounting for scr refresh
                        mask6.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask6, 'tStopRefresh')  # time at next scr refresh
                        mask6.setAutoDraw(False)
                
                # *mask7* updates
                if mask7.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask7.frameNStart = frameN  # exact frame index
                    mask7.tStart = t  # local t and not account for scr refresh
                    mask7.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask7, 'tStartRefresh')  # time at next scr refresh
                    mask7.setAutoDraw(True)
                if mask7.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask7.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask7.tStop = t  # not accounting for scr refresh
                        mask7.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask7, 'tStopRefresh')  # time at next scr refresh
                        mask7.setAutoDraw(False)
                
                # *mask8* updates
                if mask8.status == NOT_STARTED and tThisFlip >= ET+0.5-frameTolerance:
                    # keep track of start time/frame for later
                    mask8.frameNStart = frameN  # exact frame index
                    mask8.tStart = t  # local t and not account for scr refresh
                    mask8.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(mask8, 'tStartRefresh')  # time at next scr refresh
                    mask8.setAutoDraw(True)
                if mask8.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > mask8.tStartRefresh + 0.5-frameTolerance:
                        # keep track of stop time/frame for later
                        mask8.tStop = t  # not accounting for scr refresh
                        mask8.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(mask8, 'tStopRefresh')  # time at next scr refresh
                        mask8.setAutoDraw(False)
                
                # *key_resp* updates
                waitOnFlip = False
                if key_resp.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp.frameNStart = frameN  # exact frame index
                    key_resp.tStart = t  # local t and not account for scr refresh
                    key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                    key_resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > key_resp.tStartRefresh + 2.5-frameTolerance:
                        # keep track of stop time/frame for later
                        key_resp.tStop = t  # not accounting for scr refresh
                        key_resp.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(key_resp, 'tStopRefresh')  # time at next scr refresh
                        key_resp.status = FINISHED
                if key_resp.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp.getKeys(keyList=['f','j'], waitRelease=False)
                    _key_resp_allKeys.extend(theseKeys)
                    if len(_key_resp_allKeys):
                        key_resp.keys = _key_resp_allKeys[0].name  # just the first key pressed
                        key_resp.rt = _key_resp_allKeys[0].rt
                        # was this correct?
                        if (key_resp.keys == str(correctAns)) or (key_resp.keys == correctAns):
                            key_resp.corr = 1
                        else:
                            key_resp.corr = 0
                
                # *image1* updates
                if image1.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    image1.frameNStart = frameN  # exact frame index
                    image1.tStart = t  # local t and not account for scr refresh
                    image1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(image1, 'tStartRefresh')  # time at next scr refresh
                    image1.setAutoDraw(True)
                if image1.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > image1.tStartRefresh + ET-frameTolerance:
                        # keep track of stop time/frame for later
                        image1.tStop = t  # not accounting for scr refresh
                        image1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(image1, 'tStopRefresh')  # time at next scr refresh
                        image1.setAutoDraw(False)
                
                # *image2* updates
                if image2.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    image2.frameNStart = frameN  # exact frame index
                    image2.tStart = t  # local t and not account for scr refresh
                    image2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(image2, 'tStartRefresh')  # time at next scr refresh
                    image2.setAutoDraw(True)
                if image2.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > image2.tStartRefresh + ET-frameTolerance:
                        # keep track of stop time/frame for later
                        image2.tStop = t  # not accounting for scr refresh
                        image2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(image2, 'tStopRefresh')  # time at next scr refresh
                        image2.setAutoDraw(False)
                
                # *image3* updates
                if image3.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    image3.frameNStart = frameN  # exact frame index
                    image3.tStart = t  # local t and not account for scr refresh
                    image3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(image3, 'tStartRefresh')  # time at next scr refresh
                    image3.setAutoDraw(True)
                if image3.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > image3.tStartRefresh + ET-frameTolerance:
                        # keep track of stop time/frame for later
                        image3.tStop = t  # not accounting for scr refresh
                        image3.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(image3, 'tStopRefresh')  # time at next scr refresh
                        image3.setAutoDraw(False)
                
                # *image4* updates
                if image4.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    image4.frameNStart = frameN  # exact frame index
                    image4.tStart = t  # local t and not account for scr refresh
                    image4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(image4, 'tStartRefresh')  # time at next scr refresh
                    image4.setAutoDraw(True)
                if image4.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > image4.tStartRefresh + ET-frameTolerance:
                        # keep track of stop time/frame for later
                        image4.tStop = t  # not accounting for scr refresh
                        image4.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(image4, 'tStopRefresh')  # time at next scr refresh
                        image4.setAutoDraw(False)
                
                # *image5* updates
                if image5.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    image5.frameNStart = frameN  # exact frame index
                    image5.tStart = t  # local t and not account for scr refresh
                    image5.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(image5, 'tStartRefresh')  # time at next scr refresh
                    image5.setAutoDraw(True)
                if image5.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > image5.tStartRefresh + ET-frameTolerance:
                        # keep track of stop time/frame for later
                        image5.tStop = t  # not accounting for scr refresh
                        image5.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(image5, 'tStopRefresh')  # time at next scr refresh
                        image5.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "trial"-------
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp.keys in ['', [], None]:  # No response was made
                key_resp.keys = None
                # was no response the correct answer?!
                if str(correctAns).lower() == 'none':
                   key_resp.corr = 1;  # correct non-response
                else:
                   key_resp.corr = 0;  # failed to respond (incorrectly)
            # store data for trials (TrialHandler)
            trials.addData('key_resp.keys',key_resp.keys)
            trials.addData('key_resp.corr', key_resp.corr)
            if key_resp.keys != None:  # we had a response
                trials.addData('key_resp.rt', key_resp.rt)
            # update the listACC
            listACC.append([Ratio, ET, key_resp.corr])
            # the Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "feedbacks"-------
            continueRoutine = True
            routineTimer.add(2.000000)
            # update component parameters for each repeat
            # present whether the response is correct.
            msgFeedback = ''
            if expInfo['language'] == 'Chinese':
                if key_resp.corr:
                    msgFeedback = "正确!"
                else:
                    msgFeedback = "错误!!!"
            else:
                if key_resp.corr:
                    msgFeedback = "Correct!"
                else:
                    msgFeedback = "Wrong!!!"
            feedback.setText(msgFeedback)
            
            # keep track of which components have finished
            feedbacksComponents = [feedback, fix_end]
            for thisComponent in feedbacksComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            feedbacksClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "feedbacks"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = feedbacksClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=feedbacksClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *feedback* updates
                if feedback.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    feedback.frameNStart = frameN  # exact frame index
                    feedback.tStart = t  # local t and not account for scr refresh
                    feedback.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(feedback, 'tStartRefresh')  # time at next scr refresh
                    feedback.setAutoDraw(True)
                if feedback.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > feedback.tStartRefresh + 0.75-frameTolerance:
                        # keep track of stop time/frame for later
                        feedback.tStop = t  # not accounting for scr refresh
                        feedback.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(feedback, 'tStopRefresh')  # time at next scr refresh
                        feedback.setAutoDraw(False)
                
                # *fix_end* updates
                if fix_end.status == NOT_STARTED and tThisFlip >= 0.75-frameTolerance:
                    # keep track of start time/frame for later
                    fix_end.frameNStart = frameN  # exact frame index
                    fix_end.tStart = t  # local t and not account for scr refresh
                    fix_end.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fix_end, 'tStartRefresh')  # time at next scr refresh
                    fix_end.setAutoDraw(True)
                if fix_end.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > fix_end.tStartRefresh + 1.25-frameTolerance:
                        # keep track of stop time/frame for later
                        fix_end.tStop = t  # not accounting for scr refresh
                        fix_end.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(fix_end, 'tStopRefresh')  # time at next scr refresh
                        fix_end.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in feedbacksComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "feedbacks"-------
            for thisComponent in feedbacksComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            thisExp.nextEntry()
            
        # completed repN repeats of 'trials'
        
        
        # ------Prepare to start Routine "estimation"-------
        continueRoutine = True
        # update component parameters for each repeat
        key_rest.keys = []
        key_rest.rt = []
        _key_rest_allKeys = []
        # update the listECCC 
        if expInfo['task'] == 'MFT_R':
            cat = True
            dfACC = pd.DataFrame(listACC, columns = ['Ratios', 'ETs', 'ACC'])
            ECCC = getECCC(dfACC)
            listECCC.append(ECCC)
            
            # calculate the SE of the listECCC
            if len(listECCC) >= 2 and expInfo['precision'] != 'None':
                SE = np.std(listECCC) / np.sqrt(len(listECCC) - 1)
                
                # end the blockLoop when reach the SE criteria
                if len(listECCC) >= 25 and SE <= float(expInfo['precision']):
                    break
        
        
        if expInfo['task'] == 'MFT_M':
            rest = False
        else:
            rest = True
        
        msgRest = ''
        if expInfo['language'] == 'English':
            msgRest  = "Take a rest, press space bar to continue.."
            text_rest.setText(msgRest)
        # keep track of which components have finished
        estimationComponents = [key_rest, text_rest]
        for thisComponent in estimationComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        estimationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "estimation"-------
        while continueRoutine:
            # get current time
            t = estimationClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=estimationClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *key_rest* updates
            waitOnFlip = False
            if key_rest.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                key_rest.frameNStart = frameN  # exact frame index
                key_rest.tStart = t  # local t and not account for scr refresh
                key_rest.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_rest, 'tStartRefresh')  # time at next scr refresh
                key_rest.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_rest.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_rest.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_rest.status == STARTED:
                if bool(rest):
                    # keep track of stop time/frame for later
                    key_rest.tStop = t  # not accounting for scr refresh
                    key_rest.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(key_rest, 'tStopRefresh')  # time at next scr refresh
                    key_rest.status = FINISHED
            if key_rest.status == STARTED and not waitOnFlip:
                theseKeys = key_rest.getKeys(keyList=['space'], waitRelease=False)
                _key_rest_allKeys.extend(theseKeys)
                if len(_key_rest_allKeys):
                    key_rest.keys = _key_rest_allKeys[-1].name  # just the last key pressed
                    key_rest.rt = _key_rest_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *text_rest* updates
            if text_rest.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                text_rest.frameNStart = frameN  # exact frame index
                text_rest.tStart = t  # local t and not account for scr refresh
                text_rest.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_rest, 'tStartRefresh')  # time at next scr refresh
                text_rest.setAutoDraw(True)
            if text_rest.status == STARTED:
                if bool(rest):
                    # keep track of stop time/frame for later
                    text_rest.tStop = t  # not accounting for scr refresh
                    text_rest.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(text_rest, 'tStopRefresh')  # time at next scr refresh
                    text_rest.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in estimationComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "estimation"-------
        for thisComponent in estimationComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "estimation" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed blockN repeats of 'blocks'
    
# completed N repeats of 'MFTR'


# ------Prepare to start Routine "end"-------
continueRoutine = True
# update component parameters for each repeat
key_end.keys = []
key_end.rt = []
_key_end_allKeys = []
# keep track of which components have finished
endComponents = [text_end, key_end]
for thisComponent in endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end"-------
while continueRoutine:
    # get current time
    t = endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_end* updates
    if text_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_end.frameNStart = frameN  # exact frame index
        text_end.tStart = t  # local t and not account for scr refresh
        text_end.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_end, 'tStartRefresh')  # time at next scr refresh
        text_end.setAutoDraw(True)
    
    # *key_end* updates
    waitOnFlip = False
    if key_end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_end.frameNStart = frameN  # exact frame index
        key_end.tStart = t  # local t and not account for scr refresh
        key_end.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_end, 'tStartRefresh')  # time at next scr refresh
        key_end.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_end.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_end.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_end.status == STARTED and not waitOnFlip:
        theseKeys = key_end.getKeys(keyList=['space'], waitRelease=False)
        _key_end_allKeys.extend(theseKeys)
        if len(_key_end_allKeys):
            key_end.keys = _key_end_allKeys[-1].name  # just the last key pressed
            key_end.rt = _key_end_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# save the ECCC of each trial in MFT_R
if expInfo['task'] == 'MFT_R':
    trial_MFT_R = [expInfo['date'], expInfo['participant'], expInfo['session']] + listECCC
    with open('estimationResult/trial_MFT_R.csv','a',newline='') as f1:
        csvTrial= csv.writer(f1)
        csvTrial.writerow(trial_MFT_R)

# save the final ECCC of all tasks
dfACC = pd.DataFrame(listACC, columns = ['Ratios', 'ETs', 'ACC'])
CCC = getECCC(dfACC)
resultCCC = [expInfo['date'], expInfo['participant'], expInfo['session'], expInfo['task'], CCC]
with open('estimationResult/resultCCC.csv','a',newline='') as f2:
    csvResult= csv.writer(f2)
    csvResult.writerow(resultCCC)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
