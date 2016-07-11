import socket
import threading
import queue
import time
data = [0] #for testing purposes
send_port = 1235
recv_port = 1236

processing_cond = threading.Condition()

def unpackage(data):
	return data #need to replace to unpack using protobufs

def package_data(raw_state, packed, condition):
	while(True):
		if (state != None):
			condition.acquire()
			try:
				pack_state = raw_state#add actual packaging here
				packaged.replace(pack_state) #insert other mutable data structure here. Used to make it easier
				condition.notify()
			finally:
				condition.release()
		time.sleep(0.02)

def buffer_handling(packaged, condition, send_buffer):
	while(True):
		condition.acquire()
		try:
			while(True)
				pack_state = packaged.get()
				if pack_state:
					break
				condition.wait(.2)
			condition.release()
			send_buffer.replace(pack_state)
		finally:
			condition.release()
		time.sleep(0.02)



def sender(port, send_buffer):
	host = socket.gethostname()
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:#DGRAM for UDP sockets
		i = 0
		while(True):
			msg = send_buffer[i]
			s.sendto(msg, (host, send_port))
			time.sleep(0.02)

def receiver(port, receive_queue):
	#same thing as the client side from python docs
	host = socket.gethostname()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #DGRAM for UDP sockets
	#need to receive data
	#will be implemented after proof of concept
	s.bind((host, port))
	while(True):
		data, adr = s.recv(2048)
		unpackaged_data = unpackage(data)
		recv_queue.put(unpackaged_data)
		time.sleep(0.02)

recv_queue = queue.Queue()



send_thread = threading.Thread(target=sender, name = "ansible_sender", args=(send_port, send_queue))
recv_thread = threading.Thread(target=receiver, name = "ansible_receiver", args=(recv_port,  recv_queue))
send_thread.daemon = True
recv_thread.daemon = True
send_thread.start()
recv_thread.start()
fake_data = [0]

class two_buffer():
	def __init__(self, condition):
		data = [None, None]
		self.condition = condition
		self.put_index = 0
		self.get_index = 1
	def replace(self, item):
		data[self.put_index] = item
		self.put_index = (self.put_index + 1) % 2
		self.get_index = (self.get_index + 1) % 2
	def get(self):
		return data[self.get_index]
class replacable():
	def __init__(self, initial):
		self.item = initial
	def replace(item):
		self.item = item
	def get(self):
		return self.item

while(True):
	fake_data.append(1)
	send_buffer.insert(0, fake_data)
	time.sleep(0.1)
	print("waiting")
	if(not recv_queue.empty()):
		print(recv_queue.get_nowait())


	


