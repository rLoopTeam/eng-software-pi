import zmq
import sys
import time
import node_list as nl

def print_out ( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

class main():

	ctx = zmq.Context()
	cmd_receiver = ctx.socket(zmq.PULL)
	cmd_receiver.bind(nl.get_address('cmd_in'))
	cmd_sender = ctx.socket(zmq.PUSH)
	cmd_sender.bind(nl.get_address('cmd_out'))

	while True:

		try:	
			cmd_message = cmd_receiver.recv(zmq.NOBLOCK)
			print_out(cmd_message)
		except zmq.ZMQError, e:
			pass


		time.sleep(1)
			
if __name__ == "__main__":
    main = main()
