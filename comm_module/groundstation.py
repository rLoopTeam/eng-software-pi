import zmq
import sys
import time
from node_list import NodeList

def print_out ( str ):
        sys.stdout.write( str )
        sys.stdout.write( "\n" )
        sys.stdout.flush()

def main():
	
	nodeList = NodeList()
	ctx = zmq.Context()
	groundstation_receiver = ctx.socket(zmq.PULL)
	groundstation_receiver.bind(nodeList.get_node('gs_in'))
	groundstation_sender = ctx.socket(zmq.PUSH)
	groundstation_sender.bind(nodeList.get_node('gs_out'))

	while True:

		command = "MOVE_FORWARD"
		groundstation_sender.send(command)
		print_out("GS: COMMAND: %s"%command)
	
		try:
			message = groundstation_receiver.recv(zmq.NOBLOCK)
			print_out("GS: TELEMETRY: %s"%message)
		except zmq.ZMQError, e:
			pass

		time.sleep(2)


if __name__ == '__main__':
	main()
