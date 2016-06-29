import socket
import threading
import queue
import time
data = [0] #for testing purposes
send_port = 1235
recv_port = 1236
def unpackage(data):
	return data #need to replace to unpack using protobufs
def sender(port, send_queue):
	host = socket.gethostname()
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:#DGRAM for UDP sockets
		i = 0
		while(True):
			msg = send_buffer[i]
			s.sendto(msg, (host, send_port))

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

send_buffer = [None, None]
recv_queue = queue.Queue()
send_thread = threading.Thread(target=sender, name = "ansible_sender", args=(send_port, send_queue))
recv_thread = threading.Thread(target=receiver, name = "ansible_receiver", args=(recv_port,  recv_queue))
send_thread.daemon = True
recv_thread.daemon = True
send_thread.start()
recv_thread.start()
fake_data = [0]
while(True):
	fake_data.append(1)
	send_buffer.insert(fake_data, 0)
	time.sleep(0.1)
	print(recv_queue)


	


