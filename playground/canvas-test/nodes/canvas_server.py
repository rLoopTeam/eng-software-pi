import sys
import time
import zmq

def print_out ( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

def main():

	context = zmq.Context()
	
	#Set up receive and send sockets
	receiver = context.socket(zmq.PULL)
	receiver.bind("tcp://127.0.0.1:9998")

	sender = context.socket(zmq.PUB)
	sender.bind("tcp://127.0.0.1:9999")

	print_out("CANVAS server started")

	while 1:
		#Receive message from a node
	    	msg = receiver.recv()

		#Split topic (message id) and data
		topic, data = msg.split(' ', 1)

		#Broadcast message to all nodes
		sender.send("%s %s" % (topic, data))

if __name__ == '__main__':
    main()
