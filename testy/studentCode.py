import time
from runtimeUtil import *

def setup(pipe):
  pass
  # startupValue = 5
  # print("Setting Up State = %d" % (startupValue,))
  # state[0] = startupValue

def main(stateQueue, pipe):
  # while True:
  #   pass
<<<<<<< HEAD
  state
=======
  stateQueue.put([SM_COMMANDS.GET_VAL])
  response = pipe.recv()
  print("State Info:", response)
>>>>>>> origin/devel/justin
  print("Saying hello to the other side")
  state = Robot.getValue("")
  print("Hello from the other side %d" % (state,))
  1.0/state
