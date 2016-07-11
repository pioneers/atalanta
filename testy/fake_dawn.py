import socket
import threading
import queue
import time
data = [0]
send_port = 1236
recv_port = 1235

def sender(port, send_queue):
	host = socket.gethostname()
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:#DGRAM for UDP sockets
		while(True):
			msg = None
			if(not send_queue.empty):
				msg = send_queue.getnowait()
			s.sendto(msg, (host, send_port))
def receiver(port, receive_queue):
	#same thing as the client side from python docs
	host = socket.gethostname()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #DGRAM for UDP sockets
	#need to receive data
	s.bind((host, recv_port))
	while(True):
		#would actuall be:
		msg, addr = s.recvfrom(2048)
		recv_queue.putnowait(msg)

send_queue = queue.Queue()
recv_queue = queue.Queue()


send_thread = threading.Thread(target=sender, name = "fake_dawn_sender", args=(send_port, send_queue))
recv_thread = threading.Thread(target=receiver, name = "fake_dawn_receiver", args=(recv_port,  recv_queue))
send_thread.daemon = True
recv_thread.daemon = True
send_thread.start()
recv_thread.start()

while(True):
	msg = 'No message received'
	if(not recv_queue.isEmpty()):
		msg = recv_queue.getnowait()
		send_queue.putnowait(msg)

#write tests