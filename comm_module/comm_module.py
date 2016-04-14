import zmq
import time
from node_list import NodeList

def main():

	nodeList = NodeList()
	ctx = zmq.Context()
	comm_receiver = ctx.socket(zmq.PULL)
	comm_receiver.bind(nodeList.get_node('comm_out'))
	comm_sender = ctx.socket(zmq.PUSH)
	comm_sender.bind(nodeList.get_node('comm_in'))

	gs_receiver = ctx.socket(zmq.PULL)
	gs_receiver.connect(nodeList.get_node('gs_out'))
	gs_sender = ctx.socket(zmq.PUSH)
	gs_sender.connect(nodeList.get_node('gs_in'))

	cmd_sender = ctx.socket(zmq.PUSH)
	cmd_sender.connect(nodeList.get_node('cmd_in'))

	tele_receiver = ctx.socket(zmq.PULL)
	tele_receiver.connect(nodeList.get_node('tele_out'))

	while True:

		try:	
			comm_message = comm_receiver.recv(zmq.NOBLOCK)
			print("COMM: %s"%comm_message)
		except zmq.ZMQError, e:
			pass

		try:	
			gs_message = gs_receiver.recv(zmq.NOBLOCK)
			cmd_sender.send(gs_message)
			print("COMM: COMMAND: %s"%gs_message)
		except zmq.ZMQError, e:
			pass

		try:	
			tele_message = tele_receiver.recv(zmq.NOBLOCK)
			print("COMM: TELEMETRY: %s"%tele_message)
		except zmq.ZMQError, e:
			pass

		time.sleep(1)

if __name__ == '__main__':
	main()
