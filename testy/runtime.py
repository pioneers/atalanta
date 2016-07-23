import threading
import time
import sys
import traceback
import Ansible
import studentCode


STUDENT_THREAD_NAME = "student_thread"

from runtimeUtil import *

STUDENT_THREAD_NAME = "studentThread"
STUDENT_THREAD_HZ = 5 # Number of times to execute studentcode.main per second
DEBUG_DELIMITER_STRING = "****************** RUNTIME DEBUG ******************"
# TODO:
# 0. Set up testing code for the following features. 
# 1. Have student code throw an exception. Make sure runtime catches gracefully.
# 2. Have student code go through api to modify state. 
# 3. Create Error class for handling various errors/events

allThreads = {}
badThings = threading.Condition()
globalBadThing = None
#socket constants
send_port = 1235
recv_port = 1236
actual_state = {'device_id':['type', 'value']}
actual_state['robot_state'] = 2

def runtime():
  restartCount = 0
  state = [0]
  try:
    while True:
      if restartCount >= 5:
        print(DEBUG_DELIMITER_STRING)
        print("Too many restarts, terminating")
        break
      print(DEBUG_DELIMITER_STRING)
      print("Starting studentCode attempt: %s" % (restartCount,))
      runStudentCode(state)
      runAnsibleHelper(state)
      badThings.acquire()
      badThings.wait()
      print(DEBUG_DELIMITER_STRING)
      print(globalBadThing)
      badThings.release()
      restartCount += 1
  except:
    print(DEBUG_DELIMITER_STRING)
    print("Funtime Runtime Had Too Much Fun")
    print(traceback.print_exception(*sys.exc_info()))

def initRobotState(state):
  state[0] = 0

def runStudentCode(state):
  initRobotState(state)
  studentThread = threading.Thread(target=runStudentCodeHelper, name=STUDENT_THREAD_NAME, args=(state,))
  allThreads[STUDENT_THREAD_NAME] = studentThread
  studentThread.daemon = True
  studentThread.start()

def runStudentCodeHelper(state):
  global globalBadThing
  try:
    studentCode.setup(state)
    nextCall = time.time()
    while True:
      studentCode.main(state)
      nextCall += 1.0/STUDENT_THREAD_HZ
      time.sleep(nextCall - time.time())
  except Exception:
    badThings.acquire()
    globalBadThing = BadThing(sys.exc_info(), None)
    badThings.notify()
    badThings.release()

def runAnsibleHelper(state):
    global globalBadThing
    recv_queue = [[0]]
    processing_cond = threading.RLock()

    send_buffer = two_buffer(processing_cond)
    raw_fake_data = [[0]]
    packed_fake_data = [[0]]
    dawn_buffer = [0]

    try:
        pack_thread = threading.Thread(target=package_data, name = "Ansible_packager", args=(raw_fake_data, packed_fake_data, processing_cond))
        buffer_thread = threading.Thread(target=buffer_handling, name = "buffer_handler", args=(packed_fake_data, processing_cond, send_buffer))
        send_thread = threading.Thread(target=sender, name = "ansible_sender", args=(send_port, send_buffer))
        recv_thread = threading.Thread(target=receiver, name = "ansible_receiver", args=(recv_port,  recv_queue))
        send_thread.daemon = True
        recv_thread.daemon = True
        pack_thread.daemon = True
        buffer_thread.daemon = True
        pack_thread.start()
        buffer_thread.start()
        send_thread.start()
        recv_thread.start()
    except:
        badThings.acquire()
        globalBadThing = BadThing(sys.exc_info(), None)
        badThings.notify()
        badThings.release()

runtime()