import socket
import threading
import queue
import time
import runtime_proto_pb2
import fake_dawn
import random
import ansible_pb2
from runtimeUtil import *
data = [0] #for testing purposes
send_port = 1235
recv_port = 1236
stateToEnum = {0:runtime_proto_pb2.STUDENT_CRASHED,
			   1:runtime_proto_pb2.STUDENT_RUNNING,
			   2:runtime_proto_pb2.STUDENT_STOPPED,
			   3:runtime_proto_pb2.TELEOP,
			   4:runtime_proto_pb2.AUTO
				}
#Custom buffer for handling states. Holds two states, updates one and sends the other.
#If states are updated, the newest state becomes the state that is sent and the other becomes the one getting updated
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

processing_cond = threading.RLock()


###Protobuf handlers###
#Function for handling unpackaging of protobufs from Dawn
def unpackage(data):
	 dawnData = ansible_pb2.DawnData()
	 try:
	 	dawn_data.ParseFromString(data)#Change from bytes to actual data
	 	return dawn_data
	 except:#if it's a None class, TODO: handle this here instead sending a message that no data is coming from dawn
	 	return data
#Handles packaging and sending state to dawn in the form of protobuf we define
def package(state):
	proto_message = runtime_proto_pb2.RuntimeData()
	for devId, devVal in state.items(): #Parse through entire state and package it
		if(devID is 'studentCodeState'):
			proto_message.robot_state = stateToEnum[devVal] #check if we are dealing with sensor data or student code state
		else:
			test_sensor = proto_message.sensor.add() #Create new submessage for each sensor and add corresponding values
			test_sensor.id = devId
			test_sensor.type = devVal[0]
			test_sensor.value = state[1]

	return bytes(proto_message.SerializeToString()) #return the serialized data as bytes to be sent to Dawn



###Start Ansible Thread Chain###
def package_data(packed, lock, pipe, badThingsQueue):
	while(True):
		try:
			rawState = pipe.recv() #Pull state from the pipe
			if (rawState):
				with lock:
					packState = package(raw_state[0])
					packed[0]=packState ##Used list mutation as it's an atomic operation
		except Exception:
			badThingsQueue.put(BadThing(sys.exc_info(), None))

def buffer_handling(packaged, lock, sendBuffer, badThingsQueue): #made this separate since changing list locations in the buffer instance isn't atomic
	while(True):
		try:
			with lock:
				packState = packaged[0]
				sendBuffer.replace(pack_state) 
		except Exception:
			badThingsQueue.put(BadThing(sys.exc_info(), None))



def sender(port, sendBuffer, badThingsQueue):
	host = socket.gethostname()
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:#DGRAM for UDP sockets
		while(True): #constantly send the state to Dawn
			try:
				msg = sendBuffer.get() 
				s.sendto(msg, (host, send_port))
			except Exception:
				badThingsQueue.put(BadThing(sys.exc_info(), None))


def receiver(port, receivePipe, badThingsQueue):
	#same thing as the client side from python docs
	host = socket.gethostname()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #DGRAM for UDP sockets
	s.bind((host, port))
	while(True):
		try:
			data = s.recv(2048) #can be changed later if we need more 
			unpackaged_data = unpackage(data)
			receivePipe.send(unpackaged_data) #send to stateManager
		except Exception: 
			badThingsQueue.put(BadThing(sys.exc_info(), None))


def tcpSender(port, sendQueue, badThingsQueue):
	try:
		host = socket.gethostname()
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			s.listen(1)
			conn, addr = s.accept()
			with conn:
				print('Connected by', addr)
	        	while True:
	        		try:
		            	conn.sendall(sendQueue.get_nowait())
		            except QueueEmpty:
		            	pass
	except Exception:
		badThingsQueue.put(BadThing(sys.exc_info(),None))

def tcpReceiver(port, recvQueue, badThingsQueue):
	try:
		host = socket.gethostname()
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			while(True):
				recvData = s.recv(2048)
				recvQueue.put(recvData)
	except Exception:
		badThingsQueue.put(BadThing(sys.exc_info(), None))




        


		




	


