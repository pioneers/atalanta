import time

def main(state):
  print("Hello from the other side " + str(state[0]))
  print(1/0)
  state[0] += 1
