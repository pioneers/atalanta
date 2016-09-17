# import multiprocessing
import sys

from runtimeUtil import *

# TODO:
# 0. modify self.state to acually store (name, value) pairs
class StateManager(object):

  """input is a multiprocessing.Queue object to support multiple
  processes requesting state data
  """
  def __init__(self, badThingsQueue, inputQueue, runtimePipe):
    self.initRobotState()
    self.badThingsQueue = badThingsQueue
    self.input = inputQueue
    # map process names to pipes
    self.processMapping = {PROCESS_NAMES.RUNTIME: runtimePipe}

  def initRobotState(self):
    self.state = {
      'boolean': 230984,
      'int': False,
      'list': {
        'what': 1
      },
      'dictionary': [1, 2, 'hi'],
      'lambda': lambda x: x**2
    }

  def addPipe(self, processName, pipe):
    self.processMapping[processName] = pipe
    pipe.send(SM_COMMANDS.READY)

  def start(self):
    # TODO: Make sure request is a list/tuple before attempting to access
    # And that there are the correct number of elements
    while True:
      request = self.input.get(block=True)

      if request[0] == SM_COMMANDS.RESET:
        self.initRobotState()

      elif request[0] == SM_COMMANDS.ADD:
        self.addPipe(request[1], request[2])

      elif request[0] == SM_COMMANDS.HELLO:
        self.state[0] -= 1
        self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(self.state[0])
      # TODO: Add better error description
      else:
        self.badThingsQueue.put(BadThing(sys.exc_info(), "Unknown process name: %s" % (request,), event = BAD_EVENTS.UNKNOWN_PROCESS, printStackTrace = False))
