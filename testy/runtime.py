import multiprocessing
import time
import sys
import traceback
import Ansible
import studentCode
import stateManager


STUDENT_THREAD_NAME = "student_thread"

from runtimeUtil import *


# TODO:
# 0. Set up testing code for the following features.
# 1. Have student code go through api to modify state.
# 2. Imposing timeouts on student code (infinite loop, try-catch)
# 3. Figure out how to kill student thread.
# 4. Integrate with Bob's socket code: spin up a communication process
# 5. stateManager throw badThing on processNameNotFound
# 6. refactor process startup code: higher order function

allProcesses = {}
badThings = multiprocessing.Condition()
globalBadThing = "unititialized globalBadThing"
officialState = {'deviceId':['deviceType', 'value']}
officialState['studentCodeState'] = 2 

sendPort = 1235
recvPort = 1236


def runtime():
  badThingsQueue = multiprocessing.Queue()
  stateQueue = multiprocessing.Queue()
  spawnProcess = processFactory(badThingsQueue, stateQueue)
  restartCount = 0
  try:
    spawnProcess(PROCESS_NAMES.STATE_MANAGER, startStateManager)
    while True:
      if restartCount >= 5:
        print(RUNTIME_INFO.DEBUG_DELIMITER_STRING.value)
        print("Too many restarts, terminating")
        break
      print(RUNTIME_INFO.DEBUG_DELIMITER_STRING.value)
      print("Starting studentCode attempt: %s" % (restartCount,))
      spawnProcess(PROCESS_NAMES.STUDENT_CODE, runStudentCode)
      while True:
        globalBadThing = badThingsQueue.get(block=True)
        print(RUNTIME_INFO.DEBUG_DELIMITER_STRING.value)
        print(globalBadThing)
        if globalBadThing.event == BAD_EVENTS.STUDENT_CODE_ERROR:
          break
      stateQueue.put([SM_COMMANDS.RESET])
      restartCount += 1
  except:
    print(RUNTIME_INFO.DEBUG_DELIMITER_STRING.value)
    print("Funtime Runtime Had Too Much Fun")
    print(traceback.print_exception(*sys.exc_info()))

def runStudentCode(badThingsQueue, stateQueue, pipe):
  try:
    studentCode.setup(pipe)
    nextCall = time.time()
    while True:
      studentCode.main(stateQueue, pipe)
      nextCall += 1.0/RUNTIME_INFO.STUDENT_CODE_HZ.value
      time.sleep(nextCall - time.time())
  except Exception:
    badThingsQueue.put(BadThing(sys.exc_info(), None))

def runAnsibleHelper(badThingsQueue, stateQueue, sendPipe, recvPipe): #Could maybe make these 1 two-way pipe, need to be discussed.
  global globalBadThing
  processingCond = threading.RLock()

  sendBuffer = two_buffer(processingCond)
  packedData = [[0]]
  dawnBuffer = [0]

  try:
      pack_thread = threading.Thread(target=package_data, name = "Ansible_packager", args=(packedData, processingCond, sendPipe, badThingsQueue))
      buffer_thread = threading.Thread(target=buffer_handling, name = "buffer_handler", args=(packedData, processingCond, sendBuffer, badThingsQueue))
      send_thread = threading.Thread(target=sender, name = "ansible_sender", args=(sendPort, sendBuffer, badThingsQueue))
      recv_thread = threading.Thread(target=receiver, name = "ansible_receiver", args=(recvPort,  recvPipe, badThingsQueue))
      send_thread.daemon = True
      recv_thread.daemon = True
      pack_thread.daemon = True
      buffer_thread.daemon = True
      pack_thread.start()
      buffer_thread.start()
      send_thread.start()
      recv_thread.start()
  except:
      badThingsQueue.put(BadThing(sys.exc_info(), None, event=BAD_EVENTS.STUDENT_CODE_ERROR))

def startStateManager(badThingsQueue, stateQueue, runtimePipe):
  try:
    SM = stateManager.StateManager(badThingsQueue, stateQueue, runtimePipe)
    SM.start()
  except Exception:
    badThingsQueue.put(BadThing(sys.exc_info(), None))

def processFactory(badThingsQueue, stateQueue):
  def spawnProcessHelper(processName, helper):
    pipeToChild, pipeFromChild = multiprocessing.Pipe()
    if processName != PROCESS_NAMES.STATE_MANAGER:
      stateQueue.put([SM_COMMANDS.ADD, processName, pipeToChild], block=True)
    newProcess = multiprocessing.Process(target=helper, name=processName.value, args=(badThingsQueue, stateQueue, pipeFromChild))
    allProcesses[processName] = newProcess
    newProcess.daemon = True
    newProcess.start()
  return spawnProcessHelper

runtime()