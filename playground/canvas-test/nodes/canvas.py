
import zmq
import sys

class msg:
    def __init__(self, a, b):
        self.id = a
        self.data = b

#stdout print function that works well with supervisord
def print_out ( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

#init a zmq "CAN" sender
def init_sender():
	context = zmq.Context()
	sender = context.socket(zmq.PUSH)
	sender.connect("tcp://127.0.0.1:9998")
	return sender

#init a zmq "CAN" receiver
def init_receiver():
	context = zmq.Context()
	receiver = context.socket(zmq.SUB)
	receiver.connect("tcp://127.0.0.1:9999")
	return receiver

#send two strings as id, data on the CAN bus
def send(socket, msg_id, msg_data):
	socket.send("%s %s" % (msg_id, msg_data))

#send a cavas message on the CAN bus
def send_msg(socket, msg):
	socket.send("%s %s" % (msg.id, msg.data))

#blocking receive on the CAN bus
def recv(socket):
	can_message = socket.recv()
	msg_id, data = can_message.split(' ', 1)
	return msg_id, data

#non-blocking receive on the CAN bus
def recv_noblock(socket):
	try:
		can_message = socket.recv(flags=zmq.NOBLOCK)
	except zmq.error.Again, e:
		return "no_id", "no_message"
	msg_id, data = can_message.split(' ', 1)
	return msg_id, data

#add message filters to a CAN receiver
def add_id(socket, filters):
	for f in filters:
		socket.setsockopt(zmq.SUBSCRIBE, f)
	
#remove message filters from a CAN receiver
def rm_id(socket, filters):
	for f in filters:
		socket.setsockopt(zmq.UNSUBSCRIBE, f)
	
