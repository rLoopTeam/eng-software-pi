import zmq
import sys
import random
import time
import threading
from node_list import NodeList

def print_out ( str ):
        sys.stdout.write( str )
        sys.stdout.write( "\n" )
        sys.stdout.flush()

def main():

	nodeList = NodeList()
	ctx = zmq.Context()
	comm_sender = ctx.socket(zmq.PUSH)
	comm_sender.bind(nodeList.get_node('tele_out'))

	while True:
		message = str(random.random()*100)
		print_out("TELE: TELEMETRY: %s"%message)
		comm_sender.send(message)
		time.sleep(1)

if __name__ == '__main__':
	main()
