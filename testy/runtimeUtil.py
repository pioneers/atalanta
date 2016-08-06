import traceback
import multiprocessing
from enum import Enum, unique

@unique
class BAD_EVENTS(Enum):
  BAD_EVENT           = "BAD THINGS HAPPENED"
  STUDENT_CODE_ERROR  = "Student Code Crashed"
  UNKNOWN_PROCESS     = "Unknown State Manager process name"

@unique
class PROCESS_NAMES(Enum):
  STUDENT_CODE        = "studentProcess"
  STATE_MANAGER       = "stateProcess"
  RUNTIME             = "runtime"

@unique
class SM_COMMANDS(Enum):
  # Used to autoenumerate
  # Don't ask I don't know how
  # https://docs.python.org/3/library/enum.html#autonumber
  def __new__(cls):
    value = len(cls.__members__) + 1
    obj = object.__new__(cls)
    obj._value_ = value
    return obj

  RESET               = ()
  ADD                 = ()
  HELLO               = ()
  READY               = ()

class RUNTIME_INFO(Enum):
  STUDENT_CODE_HZ    = 5 # Number of times to execute studentCode.main per second
  DEBUG_DELIMITER_STRING  = "****************** RUNTIME DEBUG ******************"

class BadThing:
  def __init__(self, exc_info, data, event=BAD_EVENTS.BAD_EVENT, printStackTrace=True):
    self.name = multiprocessing.current_process().name
    self.data = data
    self.event = event
    self.errorType, self.errorValue, tb = exc_info
    self.stackTrace = self.genStackTrace(tb)
    self.printStackTrace = printStackTrace

  def genStackTrace(self, tb):
    badThingDump = \
      ("Fatal Error in thread: %s\n"
      "Bad Event: %s\n"
      "Error Type: %s\n"
      "Error Value: %s\n"
      "Traceback: \n%s") % \
<<<<<<< HEAD
      (self.name, self.event, self.errorType, self.errorValue, "".join(traceback.format_tb(self.traceback)))
    return badThingDump


class two_buffer():
  def __init__(self, condition):
    self.data = [None, None]
    self.condition = condition
    self.put_index = 0
    self.get_index = 1
  def replace(self, item):
    self.data[self.put_index] = item
    self.put_index = (self.put_index + 1) % 2
    self.get_index = (self.get_index + 1) % 2
  def get(self):
    return self.data[self.get_index]
=======
      (self.name, self.event, self.errorType, self.errorValue, "".join(traceback.format_tb(tb)))
    return badThingDump

  def __str__(self):
    if self.printStackTrace:
      return self.stackTrace
    else:
      return str(self.data)
>>>>>>> devel_yizhe
