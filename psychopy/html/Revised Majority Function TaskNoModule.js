/*************************************** 
 * Revised Majority Function Task Test *
 ***************************************/

// init psychoJS:
var psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0, 0, 0]),
  units: 'height'
});

// store info about the experiment session:
let expName = 'Revised Majority Function Task';  // from the Builder filename that created this script
let expInfo = {'language': ['English', 'Chinese'], 'participant': '', 'session': '001', 'task': ['MFT_R', 'MFT_M', 'practice'], 'precision': [None, 0.05, 0.04, 0.03, 0.02, 0.01]};

// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); }, flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(welcomeRoutineBegin);
flowScheduler.add(welcomeRoutineEachFrame);
flowScheduler.add(welcomeRoutineEnd);
const MFTRLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(MFTRLoopBegin, MFTRLoopScheduler);
flowScheduler.add(MFTRLoopScheduler);
flowScheduler.add(MFTRLoopEnd);
flowScheduler.add(endRoutineBegin);
flowScheduler.add(endRoutineEachFrame);
flowScheduler.add(endRoutineEnd);
flowScheduler.add(quitPsychoJS, '', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, '', false);

psychoJS.start({expName, expInfo});

var frameDur;
function updateInfo() {
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '3.1.5';

  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0/Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0/60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  
  return Scheduler.Event.NEXT;
}

var welcomeClock;
var text_welcome;
var text_MFT;
var text_indicate;
var image_instr;
var text_target;
var text_press;
var text_continue;
var N;
var Ratios;
var ETs;
var listECCC;
var mapACC;
var listEacc;
var listDeriv;
var mapEacc;
var mapDeriv;
var initializeClock;
var cat;
var ECCC;
var blockN;
var blockCondition;
var prepClock;
var fix_prep;
var prepare;
var pick;
var repN;
var selection;
var trialClock;
var fix_start;
var mask1;
var mask2;
var mask3;
var mask4;
var mask5;
var mask6;
var mask7;
var mask8;
var images;
var imageSet;
var shuffle;
var image1;
var image2;
var image3;
var image4;
var image5;
var feedbacksClock;
var feedback;
var fix_end;
var estimationClock;
var text_rest;
var rest;
var getEccc;
var stdError;
var endClock;
var text_end;
var globalClock;
var routineTimer;
function experimentInit() {
  // Initialize components for Routine "welcome"
  welcomeClock = new util.Clock();
  text_welcome = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_welcome',
    text: '欢迎参加实验',
    font: 'Arial',
    units : undefined, 
    pos: [0, 0], height: 0.07,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: 0.0 
  });
  
  text_MFT = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_MFT',
    text: 'Majority Function Task\n',
    font: 'Arial',
    units : undefined, 
    pos: [0, 0.3], height: 0.08,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -1.0 
  });
  
  text_indicate = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_indicate',
    text: '屏幕上会呈现3或5个箭头，这些箭头可能指向左也可能指向右',
    font: 'Arial',
    units : undefined, 
    pos: [0, 0.22], height: 0.04,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -2.0 
  });
  
  image_instr = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image_instr', units : undefined, 
    image : 'image/instr.png', mask : undefined,
    ori : 0, pos : [0, 0.02], size : [1.2, 0.4],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -3.0 
  });
  text_target = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_target',
    text: '你的任务是指出在屏幕上所呈现的箭头中，大多数箭头所指的方向',
    font: 'Arial',
    units : undefined, 
    pos: [0, (- 0.2)], height: 0.04,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -5.0 
  });
  
  text_press = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_press',
    text: '如果判断多数箭头方向为左请按F键，判断为右请按J键',
    font: 'Arial',
    units : undefined, 
    pos: [0, (- 0.32)], height: 0.04,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -6.0 
  });
  
  text_continue = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_continue',
    text: '按空格继续...',
    font: 'Arial',
    units : undefined, 
    pos: [0, (- 0.42)], height: 0.05,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -7.0 
  });
  
  // initialize the parameters:
  N = 1;
  if (expInfo['task'] == 'MFT_R'){
      N = 2;
  } else{
      N = 1;
  }
  Ratios = ['ratio32', 'ratio41', 'ratio21'];
  ETs = [0.25, 0.5, 1, 2];
  listECCC = []
  if (expInfo['task'] == 'MFT_M') {
      Ratios = ['ratio32', 'ratio41', 'ratio21', 'ratio30', 'ratio50', 'ratio10'];
  }
  mapACC = new Map();
  for (let i of Ratios){
      for (let j of ETs) {
          var acc = []
          mapACC.set([i,j].join(),acc)
      }
  }
  
  
  // generate the map of Eacc and Deriv from the list:
  listEacc = [];
  $.ajax({
    url: 'resources/listEacc.txt',
    dataType: 'text',
    async: false,
  }).done(function(data){
      listEacc = eval(data);
  });
  listDeriv = []
  $.ajax({
    url: 'resources/listDeriv.txt',
    dataType: 'text',
    async: false,
  }).done(function(data){
      listDeriv = eval(data);
  });
  mapEacc = new Map();
  listEacc.forEach(element => {
      mapEacc.set(element[0].join(), element[1])
  });
  mapDeriv = new Map();
  listDeriv.forEach(element => {
      mapDeriv.set(element[0].join(), element[1])
  });
  // Initialize components for Routine "initialize"
  initializeClock = new util.Clock();
  cat = false;
  ECCC = false;
  blockN = 1;
  blockCondition = undefined;
  // Initialize components for Routine "prep"
  prepClock = new util.Clock();
  fix_prep = new visual.ImageStim({
    win : psychoJS.window,
    name : 'fix_prep', units : undefined, 
    image : 'image/fix.png', mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : 0.0 
  });
  prepare = true;
  pick = ':';
  repN = 1;
  
  // pick the condition according to ECCC:
  selection = function(c){
      var listDeriv = []
      var sumDeriv = 0
      for (let i of Ratios) {
          for (let j of ETs) {
              var deriv = mapEacc.get([c, i, j].join())
              sumDeriv = deriv + sumDeriv
              listDeriv.push(deriv)
          }
      }
      var temp = Math.random() * sumDeriv
      var curr_sum = 0
      var ret = undefined
      for (let n = 0; n < 12; n++){
          curr_sum = listDeriv[n] + curr_sum
          if (temp <= curr_sum) {
              ret = n.toString() + ':' + (n+1).toString()
              break
          }
      }
      return ret
  }
  // Initialize components for Routine "trial"
  trialClock = new util.Clock();
  fix_start = new visual.ImageStim({
    win : psychoJS.window,
    name : 'fix_start', units : undefined, 
    image : 'image/fix.png', mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : 0.0 
  });
  mask1 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask1', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [0.2, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -1.0 
  });
  mask2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask2', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [0.13, 0.13], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -2.0 
  });
  mask3 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask3', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [0, 0.2], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -3.0 
  });
  mask4 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask4', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [(- 0.13), 0.13], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -4.0 
  });
  mask5 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask5', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [(- 0.2), 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -5.0 
  });
  mask6 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask6', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [(- 0.13), (- 0.13)], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -6.0 
  });
  mask7 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask7', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [0, (- 0.2)], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -7.0 
  });
  mask8 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'mask8', units : undefined, 
    image : 'image/mask.png', mask : undefined,
    ori : 0, pos : [0.13, (- 0.13)], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -8.0 
  });
  images = [undefined, undefined, undefined, undefined, undefined];
  
  // change the images according to the amount of arrows(left, right):
  imageSet = function(leftN, rightN) {
      var images = ['image/none.png', 'image/none.png', 'image/none.png', 'image/none.png', 'image/none.png'];
      var i = 0;
      var j = 0;
      for (i = 0; i < leftN; i++) {
          images[i] = 'image/left.png';
      }
      for (j = 0; j < rightN; j++) {
          images[j+i] = 'image/right.png';
      }
      return images;
  }
  
  // randomize the order of a list:
  shuffle = function(array) {
      var len = array.length;
      for (var i = len -1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
  }
  
  
  image1 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image1', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -11.0 
  });
  image2 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image2', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -12.0 
  });
  image3 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image3', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -13.0 
  });
  image4 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image4', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -14.0 
  });
  image5 = new visual.ImageStim({
    win : psychoJS.window,
    name : 'image5', units : undefined, 
    image : undefined, mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -15.0 
  });
  // Initialize components for Routine "feedbacks"
  feedbacksClock = new util.Clock();
  feedback = new visual.TextStim({
    win: psychoJS.window,
    name: 'feedback',
    text: '正确',
    font: 'Arial',
    units : undefined, 
    pos: [0, 0], height: 0.08,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: 0.0 
  });
  
  fix_end = new visual.ImageStim({
    win : psychoJS.window,
    name : 'fix_end', units : undefined, 
    image : 'image/fix.png', mask : undefined,
    ori : 0, pos : [0, 0], size : [0.06, 0.06],
    color : new util.Color([1, 1, 1]), opacity : 1,
    flipHoriz : false, flipVert : false,
    texRes : 128, interpolate : true, depth : -1.0 
  });
  // Initialize components for Routine "estimation"
  estimationClock = new util.Clock();
  text_rest = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_rest',
    text: '休息片刻，可按空格跳过',
    font: 'Arial',
    units : undefined, 
    pos: [0, 0], height: 0.08,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: -1.0 
  });
  
  rest = true;
  
  // ECCC estimation using the accuracy matrix (maximun likelihood estimation):
  getEccc = function(mapACC){
      var ECCC = 0;
      var lastL = 0;
      for (let n = 0; n < 1000; n++) {
          var c = n/100;
          var lnL = Math.log(1);
          for (let i of Ratios){
              for (let j of ETs) {
                  var listACC = mapACC.get([i,j].join());
                  var meanACC = listACC.reduce((a, b) => a + b) / listACC.length;
                  if (meanACC == 1){
                      meanACC = 0.999;
                  } else if (meanACC == 0){
                      meanACC = 0.001;
                  }
                  var Eacc = mapEacc.get([c, i, j].join());
                  lnL = meanACC * Math.log(Eacc) + (1 - meanACC) * Math.log(1 - Eacc) + lnL;
              }
          }
          var L = -2 * lnL;
          if (!lastL) {
              lastL = L;
              ECCC = c;
          }else if (L < lastL){
              lastL = L;
              ECCC = c;
          }
      }
      return ECCC;
  }
  
  // calculate the stdError from a list:
  stdError = function(list){
      var mean = list.reduce((a, b) => a + b) / list.length;
      var stdDev = Math.sqrt(list.map(n=> (n-mean) * (n-mean)).reduce((a, b) => a + b) / list.length);
      var SE = stdDev / Math.sqrt(list.length - 1)
      return SE;
  }
  // Initialize components for Routine "end"
  endClock = new util.Clock();
  text_end = new visual.TextStim({
    win: psychoJS.window,
    name: 'text_end',
    text: 'The end',
    font: 'Arial',
    units : undefined, 
    pos: [0, 0], height: 0.08,  wrapWidth: undefined, ori: 0,
    color: new util.Color('black'),  opacity: 1,
    depth: 0.0 
  });
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}

var t;
var frameN;
var key_welcome;
var msg0;
var msg1;
var msg2;
var msg3;
var msg4;
var welcomeComponents;
function welcomeRoutineBegin() {
  //------Prepare to start Routine 'welcome'-------
  t = 0;
  welcomeClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  key_welcome = new core.BuilderKeyResponse(psychoJS);
  
  var msg0 = '';
  var msg1 = '';
  var msg2 = '';
  var msg3 = '';
  var msg4 = '';
  if (expInfo['language'] == 'English'){
      msg0 = 'welcome to the experiment';
      msg1 = "Several arrows would be shown on the screen pointing left or right, for example:";
      msg2 = 'Your task is to indicate the direction of the majority arrows pointed.';
      msg3 = "Press the 'F' button if the direction was left, or the 'J' button if the direction was right.";
      msg4 = 'Press space bar to continue...';
      text_welcome.setText(msg0)
      text_indicate.setText(msg1);
      text_target.setText(msg2);
      text_press.setText(msg3);
      text_continue.setText(msg4);
  }
  
  // keep track of which components have finished
  welcomeComponents = [];
  welcomeComponents.push(text_welcome);
  welcomeComponents.push(text_MFT);
  welcomeComponents.push(text_indicate);
  welcomeComponents.push(image_instr);
  welcomeComponents.push(key_welcome);
  welcomeComponents.push(text_target);
  welcomeComponents.push(text_press);
  welcomeComponents.push(text_continue);
  
  welcomeComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}

var frameRemains;
var continueRoutine;
function welcomeRoutineEachFrame() {
  //------Loop for each frame of Routine 'welcome'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = welcomeClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *text_welcome* updates
  if (t >= 0.0 && text_welcome.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_welcome.tStart = t;  // (not accounting for frame time here)
    text_welcome.frameNStart = frameN;  // exact frame index
    text_welcome.setAutoDraw(true);
  }

  frameRemains = 0.0 + 1 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (text_welcome.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    text_welcome.setAutoDraw(false);
  }
  
  // *text_MFT* updates
  if (t >= 1 && text_MFT.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_MFT.tStart = t;  // (not accounting for frame time here)
    text_MFT.frameNStart = frameN;  // exact frame index
    text_MFT.setAutoDraw(true);
  }

  
  // *text_indicate* updates
  if (t >= 1 && text_indicate.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_indicate.tStart = t;  // (not accounting for frame time here)
    text_indicate.frameNStart = frameN;  // exact frame index
    text_indicate.setAutoDraw(true);
  }

  
  // *image_instr* updates
  if (t >= 1 && image_instr.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    image_instr.tStart = t;  // (not accounting for frame time here)
    image_instr.frameNStart = frameN;  // exact frame index
    image_instr.setAutoDraw(true);
  }

  
  // *key_welcome* updates
  if (t >= 1.5 && key_welcome.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_welcome.tStart = t;  // (not accounting for frame time here)
    key_welcome.frameNStart = frameN;  // exact frame index
    key_welcome.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  if (key_welcome.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['space']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
      psychoJS.experiment.experimentEnded = true;
    }
    
    if (theseKeys.length > 0) {  // at least one key was pressed
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  
  // *text_target* updates
  if (t >= 1 && text_target.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_target.tStart = t;  // (not accounting for frame time here)
    text_target.frameNStart = frameN;  // exact frame index
    text_target.setAutoDraw(true);
  }

  
  // *text_press* updates
  if (t >= 1 && text_press.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_press.tStart = t;  // (not accounting for frame time here)
    text_press.frameNStart = frameN;  // exact frame index
    text_press.setAutoDraw(true);
  }

  
  // *text_continue* updates
  if (t >= 1 && text_continue.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_continue.tStart = t;  // (not accounting for frame time here)
    text_continue.frameNStart = frameN;  // exact frame index
    text_continue.setAutoDraw(true);
  }

  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  welcomeComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function welcomeRoutineEnd() {
  //------Ending Routine 'welcome'-------
  welcomeComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  // the Routine "welcome" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var MFTR;
var currentLoop;
var trialIterator;
function MFTRLoopBegin(thisScheduler) {
  // set up handler to look after randomisation of conditions etc
  MFTR = new TrialHandler({
    psychoJS: psychoJS,
    nReps: N, method: TrialHandler.Method.RANDOM,
    extraInfo: expInfo, originPath: undefined,
    trialList: undefined,
    seed: undefined, name: 'MFTR'});
  psychoJS.experiment.addLoop(MFTR); // add the loop to the experiment
  currentLoop = MFTR;  // we're now the current loop

  // Schedule all the trials in the trialList:
  trialIterator = MFTR[Symbol.iterator]();
  while(true) {
    let result = trialIterator.next();
    if (result.done);
      break;
    let thisMFTR = result.value;
    thisScheduler.add(importConditions(MFTR));
    thisScheduler.add(initializeRoutineBegin);
    thisScheduler.add(initializeRoutineEachFrame);
    thisScheduler.add(initializeRoutineEnd);
    const blocksLoopScheduler = new Scheduler(psychoJS);
    thisScheduler.add(blocksLoopBegin, blocksLoopScheduler);
    thisScheduler.add(blocksLoopScheduler);
    thisScheduler.add(blocksLoopEnd);
  }

  return Scheduler.Event.NEXT;
}

var blocks;
function blocksLoopBegin(thisScheduler) {
  // set up handler to look after randomisation of conditions etc
  blocks = new TrialHandler({
    psychoJS: psychoJS,
    nReps: blockN, method: TrialHandler.Method.RANDOM,
    extraInfo: expInfo, originPath: undefined,
    trialList: blockCondition,
    seed: undefined, name: 'blocks'});
  psychoJS.experiment.addLoop(blocks); // add the loop to the experiment
  currentLoop = blocks;  // we're now the current loop

  // Schedule all the trials in the trialList:
  trialIterator = blocks[Symbol.iterator]();
  while(true) {
    let result = trialIterator.next();
    if (result.done);
      break;
    let thisBlock = result.value;
    thisScheduler.add(importConditions(blocks));
    thisScheduler.add(prepRoutineBegin);
    thisScheduler.add(prepRoutineEachFrame);
    thisScheduler.add(prepRoutineEnd);
    const trialsLoopScheduler = new Scheduler(psychoJS);
    thisScheduler.add(trialsLoopBegin, trialsLoopScheduler);
    thisScheduler.add(trialsLoopScheduler);
    thisScheduler.add(trialsLoopEnd);
    thisScheduler.add(estimationRoutineBegin);
    thisScheduler.add(estimationRoutineEachFrame);
    thisScheduler.add(estimationRoutineEnd);
  }

  return Scheduler.Event.NEXT;
}

var trials;
function trialsLoopBegin(thisScheduler) {
  // set up handler to look after randomisation of conditions etc
  trials = new TrialHandler({
    psychoJS: psychoJS,
    nReps: repN, method: TrialHandler.Method.RANDOM,
    extraInfo: expInfo, originPath: undefined,
    trialList: TrialHandler.importConditions(psychoJS.serverManager, trailCondition, pick),
    seed: undefined, name: 'trials'});
  psychoJS.experiment.addLoop(trials); // add the loop to the experiment
  currentLoop = trials;  // we're now the current loop

  // Schedule all the trials in the trialList:
  trialIterator = trials[Symbol.iterator]();
  while(true) {
    let result = trialIterator.next();
    if (result.done);
      break;
    let thisTrial = result.value;
    thisScheduler.add(importConditions(trials));
    thisScheduler.add(trialRoutineBegin);
    thisScheduler.add(trialRoutineEachFrame);
    thisScheduler.add(trialRoutineEnd);
    thisScheduler.add(feedbacksRoutineBegin);
    thisScheduler.add(feedbacksRoutineEachFrame);
    thisScheduler.add(feedbacksRoutineEnd);
    thisScheduler.add(endLoopIteration(thisScheduler, thisTrial));
  }

  return Scheduler.Event.NEXT;
}


function trialsLoopEnd() {
  psychoJS.experiment.removeLoop(trials);

  return Scheduler.Event.NEXT;
}


function blocksLoopEnd() {
  psychoJS.experiment.removeLoop(blocks);

  return Scheduler.Event.NEXT;
}


function MFTRLoopEnd() {
  psychoJS.experiment.removeLoop(MFTR);

  return Scheduler.Event.NEXT;
}

var initializeComponents;
function initializeRoutineBegin() {
  //------Prepare to start Routine 'initialize'-------
  t = 0;
  initializeClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  if (expInfo['task'] == 'MFT_M'){
      blockN = 1;
      blockCondition = 'conditions/MFT_M_blocks.xlsx';
  } else {
      blockCondition = 'conditions/MFT_R_blocks.xlsx';
      if (expInfo['task'] == 'practice') {
          blockN = 8;
      }else if (expInfo['task'] == 'MFT_R' && cat == false){
          blockN = 1;
      }else{
          blockN = 192;
      }
  }
  // keep track of which components have finished
  initializeComponents = [];
  
  initializeComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}


function initializeRoutineEachFrame() {
  //------Loop for each frame of Routine 'initialize'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = initializeClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  initializeComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function initializeRoutineEnd() {
  //------Ending Routine 'initialize'-------
  initializeComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  // the Routine "initialize" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var prepTime;
var prepComponents;
function prepRoutineBegin() {
  //------Prepare to start Routine 'prep'-------
  t = 0;
  prepClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  if (prepare == true){
      prepTime = 2;
  } else {
      prepTime = 0;
  }
  // keep track of which components have finished
  prepComponents = [];
  prepComponents.push(fix_prep);
  
  prepComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}


function prepRoutineEachFrame() {
  //------Loop for each frame of Routine 'prep'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = prepClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *fix_prep* updates
  if (t >= 0 && fix_prep.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    fix_prep.tStart = t;  // (not accounting for frame time here)
    fix_prep.frameNStart = frameN;  // exact frame index
    fix_prep.setAutoDraw(true);
  }

  frameRemains = 0 + prepTime - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (fix_prep.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    fix_prep.setAutoDraw(false);
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  prepComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function prepRoutineEnd() {
  //------Ending Routine 'prep'-------
  prepComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  if (expInfo['task'] == 'MFT_M'){
      repN = 1;
      pick = ':';
  } else if (expInfo['task'] == 'practice'){
      repN = 1;
      pick = ':';
      prepare = false;
  } else {
      prepare = false;
      if (cat == false){
          repN = 2;
          pick = ':';
      } else {
          repN = 1;
          pick = selection(ECCC);
      }
  }
  // the Routine "prep" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var key_resp;
var correctAns;
var positions;
var trialComponents;
function trialRoutineBegin() {
  //------Prepare to start Routine 'trial'-------
  t = 0;
  trialClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  key_resp = new core.BuilderKeyResponse(psychoJS);
  
  // randomnize the correctAns
  var correctRand = Math.random();
  if (correctRand < 0.5){
      correctAns = 'f';
  }else{
      correctAns = 'j';
  }
  
  psychoJS.experiment.addData('pickIndex',pick);
  psychoJS.experiment.addData('correctAns.keys',correctAns);
  
  //  set the images according to the ratio of the trial
  var majorN = parseInt(Ratio[5]);
  var minorN = parseInt(Ratio[6]);
  if (correctAns == 'f'){
      images = imageSet(majorN, minorN);
  } else {
      images = imageSet(minorN, majorN);
  }
  image1.image = images[0]
  image2.image = images[1];
  image3.image = images[2];
  image4.image = images[3];
  image5.image = images[4];
  
  var positions = [[0.2, 0], [0.13, 0.13], [0, 0.2], [-0.13, 0.13], [-0.2, 0], [-0.13, -0.13], [0, -0.2], [0.13, -0.13]];
  positions = shuffle(positions);
  image1.pos = positions[0];
  image2.pos = positions[1];
  image3.pos = positions[2];
  image4.pos = positions[3];
  image5.pos = positions[4];
  // keep track of which components have finished
  trialComponents = [];
  trialComponents.push(fix_start);
  trialComponents.push(mask1);
  trialComponents.push(mask2);
  trialComponents.push(mask3);
  trialComponents.push(mask4);
  trialComponents.push(mask5);
  trialComponents.push(mask6);
  trialComponents.push(mask7);
  trialComponents.push(mask8);
  trialComponents.push(key_resp);
  trialComponents.push(image1);
  trialComponents.push(image2);
  trialComponents.push(image3);
  trialComponents.push(image4);
  trialComponents.push(image5);
  
  trialComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}


function trialRoutineEachFrame() {
  //------Loop for each frame of Routine 'trial'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = trialClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *fix_start* updates
  if (t >= 0.0 && fix_start.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    fix_start.tStart = t;  // (not accounting for frame time here)
    fix_start.frameNStart = frameN;  // exact frame index
    fix_start.setAutoDraw(true);
  }

  frameRemains = 0.0 + 3 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (fix_start.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    fix_start.setAutoDraw(false);
  }
  
  // *mask1* updates
  if (t >= (ET + 0.5) && mask1.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask1.tStart = t;  // (not accounting for frame time here)
    mask1.frameNStart = frameN;  // exact frame index
    mask1.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask1.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask1.setAutoDraw(false);
  }
  
  // *mask2* updates
  if (t >= (ET + 0.5) && mask2.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask2.tStart = t;  // (not accounting for frame time here)
    mask2.frameNStart = frameN;  // exact frame index
    mask2.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask2.setAutoDraw(false);
  }
  
  // *mask3* updates
  if (t >= (ET + 0.5) && mask3.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask3.tStart = t;  // (not accounting for frame time here)
    mask3.frameNStart = frameN;  // exact frame index
    mask3.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask3.setAutoDraw(false);
  }
  
  // *mask4* updates
  if (t >= (ET + 0.5) && mask4.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask4.tStart = t;  // (not accounting for frame time here)
    mask4.frameNStart = frameN;  // exact frame index
    mask4.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask4.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask4.setAutoDraw(false);
  }
  
  // *mask5* updates
  if (t >= (ET + 0.5) && mask5.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask5.tStart = t;  // (not accounting for frame time here)
    mask5.frameNStart = frameN;  // exact frame index
    mask5.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask5.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask5.setAutoDraw(false);
  }
  
  // *mask6* updates
  if (t >= (ET + 0.5) && mask6.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask6.tStart = t;  // (not accounting for frame time here)
    mask6.frameNStart = frameN;  // exact frame index
    mask6.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask6.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask6.setAutoDraw(false);
  }
  
  // *mask7* updates
  if (t >= (ET + 0.5) && mask7.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask7.tStart = t;  // (not accounting for frame time here)
    mask7.frameNStart = frameN;  // exact frame index
    mask7.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask7.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask7.setAutoDraw(false);
  }
  
  // *mask8* updates
  if (t >= (ET + 0.5) && mask8.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    mask8.tStart = t;  // (not accounting for frame time here)
    mask8.frameNStart = frameN;  // exact frame index
    mask8.setAutoDraw(true);
  }

  frameRemains = (ET + 0.5) + 0.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (mask8.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    mask8.setAutoDraw(false);
  }
  
  // *key_resp* updates
  if (t >= 0.5 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_resp.tStart = t;  // (not accounting for frame time here)
    key_resp.frameNStart = frameN;  // exact frame index
    key_resp.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); }); // t = 0 on screen flip
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  frameRemains = 0.5 + 2.5 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (key_resp.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    key_resp.status = PsychoJS.Status.FINISHED;
  }

  if (key_resp.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['f', 'j']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
      psychoJS.experiment.experimentEnded = true;
    }
    
    if (theseKeys.length > 0) {  // at least one key was pressed
      if (key_resp.keys.length === 0) {  // then this was the first keypress
        key_resp.keys = theseKeys[0];  // just the first key pressed
        key_resp.rt = key_resp.clock.getTime();
        // was this 'correct'?
        if (key_resp.keys == correctAns) {
            key_resp.corr = 1;
        } else {
            key_resp.corr = 0;
        }
      }
    }
  }
  
  
  // *image1* updates
  if (t >= 0.5 && image1.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    image1.tStart = t;  // (not accounting for frame time here)
    image1.frameNStart = frameN;  // exact frame index
    image1.setAutoDraw(true);
  }

  frameRemains = 0.5 + ET - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (image1.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    image1.setAutoDraw(false);
  }
  
  // *image2* updates
  if (t >= 0.5 && image2.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    image2.tStart = t;  // (not accounting for frame time here)
    image2.frameNStart = frameN;  // exact frame index
    image2.setAutoDraw(true);
  }

  frameRemains = 0.5 + ET - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (image2.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    image2.setAutoDraw(false);
  }
  
  // *image3* updates
  if (t >= 0.5 && image3.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    image3.tStart = t;  // (not accounting for frame time here)
    image3.frameNStart = frameN;  // exact frame index
    image3.setAutoDraw(true);
  }

  frameRemains = 0.5 + ET - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (image3.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    image3.setAutoDraw(false);
  }
  
  // *image4* updates
  if (t >= 0.5 && image4.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    image4.tStart = t;  // (not accounting for frame time here)
    image4.frameNStart = frameN;  // exact frame index
    image4.setAutoDraw(true);
  }

  frameRemains = 0.5 + ET - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (image4.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    image4.setAutoDraw(false);
  }
  
  // *image5* updates
  if (t >= 0.5 && image5.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    image5.tStart = t;  // (not accounting for frame time here)
    image5.frameNStart = frameN;  // exact frame index
    image5.setAutoDraw(true);
  }

  frameRemains = 0.5 + ET - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (image5.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    image5.setAutoDraw(false);
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  trialComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function trialRoutineEnd() {
  //------Ending Routine 'trial'-------
  trialComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  
  // check responses
  if (key_resp.keys === undefined || key_resp.keys.length === 0) {    // No response was made
      key_resp.keys = undefined;
  }
  
  // was no response the correct answer?!
  if (key_resp.keys === undefined) {
    if (['None','none',undefined].includes(correctAns)) {
       key_resp.corr = 1  // correct non-response
    } else {
       key_resp.corr = 0  // failed to respond (incorrectly)
    }
  }
  // store data for thisExp (ExperimentHandler)
  psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
  psychoJS.experiment.addData('key_resp.corr', key_resp.corr);
  if (typeof key_resp.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
      }
  
  // update the listACC
  mapACC.get([Ratio, ET].join()).push(key_resp.corr)
  
  // the Routine "trial" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var msgFeedback;
var feedbacksComponents;
function feedbacksRoutineBegin() {
  //------Prepare to start Routine 'feedbacks'-------
  t = 0;
  feedbacksClock.reset(); // clock
  frameN = -1;
  routineTimer.add(2.000000);
  // update component parameters for each repeat
  var msgFeedback = '';
  if (expInfo['language'] == 'Chinese'){
      if (key_resp.corr){
          msgFeedback = "正确!";
      } else{
          msgFeedback = "错误!!!";
      }
  } else {
      if (key_resp.corr){
          msgFeedback = "Correct!";
      } else{
          msgFeedback = "Wrong!!!";
      }
  }
  feedback.setText(msgFeedback);
  // keep track of which components have finished
  feedbacksComponents = [];
  feedbacksComponents.push(feedback);
  feedbacksComponents.push(fix_end);
  
  feedbacksComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}


function feedbacksRoutineEachFrame() {
  //------Loop for each frame of Routine 'feedbacks'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = feedbacksClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *feedback* updates
  if (t >= 0.0 && feedback.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    feedback.tStart = t;  // (not accounting for frame time here)
    feedback.frameNStart = frameN;  // exact frame index
    feedback.setAutoDraw(true);
  }

  frameRemains = 0.0 + 0.75 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (feedback.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    feedback.setAutoDraw(false);
  }
  
  // *fix_end* updates
  if (t >= 0.75 && fix_end.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    fix_end.tStart = t;  // (not accounting for frame time here)
    fix_end.frameNStart = frameN;  // exact frame index
    fix_end.setAutoDraw(true);
  }

  frameRemains = 0.75 + 1.25 - psychoJS.window.monitorFramePeriod * 0.75;  // most of one frame period left
  if (fix_end.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    fix_end.setAutoDraw(false);
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  feedbacksComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine && routineTimer.getTime() > 0) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function feedbacksRoutineEnd() {
  //------Ending Routine 'feedbacks'-------
  feedbacksComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  return Scheduler.Event.NEXT;
}

var key_rest;
var msgRest;
var estimationComponents;
function estimationRoutineBegin() {
  //------Prepare to start Routine 'estimation'-------
  t = 0;
  estimationClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  key_rest = new core.BuilderKeyResponse(psychoJS);
  
  // update the listECCC
  if (expInfo['task'] == 'MFT_R'){
      cat = true;
      ECCC = getEccc(mapACC);
      listECCC.push(ECCC);
      
      // calculate the SE of the listECCC
      if (listECCC.length >= 2 && expInfo['precision'] != 'None'){
          var SE = stdError(listECCC);
          
          // end the blockLoop when reach the SE criteria
          if (listECCC.length >= 25 && SE <= parseFloat(expInfo['precision'])){
              psychoJS.experiment.removeLoop(trials);
              psychoJS.experiment.removeLoop(blocks);
              psychoJS.experiment.removeLoop(MFTR);
              return Scheduler.Event.QUIT;
          }
      }
  }
  
  
  if (expInfo['task'] == 'MFT_M'){
      rest = false;
  }else{
      rest = true;
  }
  
  var msgRest = ''
  if (expInfo['language'] == 'English'){
      msgRest  = "Take a rest, press space bar to continue.."
      text_rest.setText(msgRest)
  }
  // keep track of which components have finished
  estimationComponents = [];
  estimationComponents.push(key_rest);
  estimationComponents.push(text_rest);
  
  estimationComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}


function estimationRoutineEachFrame() {
  //------Loop for each frame of Routine 'estimation'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = estimationClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *key_rest* updates
  if (t >= 0 && key_rest.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_rest.tStart = t;  // (not accounting for frame time here)
    key_rest.frameNStart = frameN;  // exact frame index
    key_rest.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  if (key_rest.status === PsychoJS.Status.STARTED && Boolean(rest)) {
    key_rest.status = PsychoJS.Status.FINISHED;
  }

  if (key_rest.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['space']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
      psychoJS.experiment.experimentEnded = true;
    }
    
    if (theseKeys.length > 0) {  // at least one key was pressed
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  
  // *text_rest* updates
  if (t >= 0 && text_rest.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_rest.tStart = t;  // (not accounting for frame time here)
    text_rest.frameNStart = frameN;  // exact frame index
    text_rest.setAutoDraw(true);
  }

  if (text_rest.status === PsychoJS.Status.STARTED && Boolean(rest)) {
    text_rest.setAutoDraw(false);
  }
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  estimationComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function estimationRoutineEnd() {
  //------Ending Routine 'estimation'-------
  estimationComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  // the Routine "estimation" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}

var key_end;
var endComponents;
function endRoutineBegin() {
  //------Prepare to start Routine 'end'-------
  t = 0;
  endClock.reset(); // clock
  frameN = -1;
  // update component parameters for each repeat
  key_end = new core.BuilderKeyResponse(psychoJS);
  
  // keep track of which components have finished
  endComponents = [];
  endComponents.push(text_end);
  endComponents.push(key_end);
  
  endComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
     });
  
  return Scheduler.Event.NEXT;
}


function endRoutineEachFrame() {
  //------Loop for each frame of Routine 'end'-------
  let continueRoutine = true; // until we're told otherwise
  // get current time
  t = endClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *text_end* updates
  if (t >= 0.0 && text_end.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    text_end.tStart = t;  // (not accounting for frame time here)
    text_end.frameNStart = frameN;  // exact frame index
    text_end.setAutoDraw(true);
  }

  
  // *key_end* updates
  if (t >= 0.0 && key_end.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_end.tStart = t;  // (not accounting for frame time here)
    key_end.frameNStart = frameN;  // exact frame index
    key_end.status = PsychoJS.Status.STARTED;
    // keyboard checking is just starting
    psychoJS.eventManager.clearEvents({eventType:'keyboard'});
  }

  if (key_end.status === PsychoJS.Status.STARTED) {
    let theseKeys = psychoJS.eventManager.getKeys({keyList:['space']});
    
    // check for quit:
    if (theseKeys.indexOf('escape') > -1) {
      psychoJS.experiment.experimentEnded = true;
    }
    
    if (theseKeys.length > 0) {  // at least one key was pressed
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return psychoJS.quit('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  endComponents.forEach( function(thisComponent) {
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
    }});
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  }
  else {
    return Scheduler.Event.NEXT;
  }
}


function endRoutineEnd() {
  //------Ending Routine 'end'-------
  endComponents.forEach( function(thisComponent) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }});
  // the Routine "end" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  return Scheduler.Event.NEXT;
}


function endLoopIteration(thisScheduler, thisTrial) {
  // ------Prepare for next entry------
  return function () {
    // ------Check if user ended loop early------
    if (currentLoop.finished) {
      // Check for and save orphaned data
      if (Object.keys(psychoJS.experiment._thisEntry).length > 0) {
        psychoJS.experiment.nextEntry();
      }
      thisScheduler.stop();
    } else if (typeof thisTrial === 'undefined' || !('isTrials' in thisTrial) || thisTrial.isTrials) {
      psychoJS.experiment.nextEntry();
    }
  return Scheduler.Event.NEXT;
  };
}


function importConditions(loop) {
  const trialIndex = loop.getTrialIndex();
  return function () {
    loop.setTrialIndex(trialIndex);
    psychoJS.importAttributes(loop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}


function quitPsychoJS(message, isCompleted) {
  // Check for and save orphaned data
  if (Object.keys(psychoJS.experiment._thisEntry).length > 0) {
    psychoJS.experiment.nextEntry();
  }
  psychoJS.window.close();
  psychoJS.quit({message: message, isCompleted: isCompleted});

  return Scheduler.Event.QUIT;
}
