import zmq
import time
from node_list import NodeList

class main():

	nodeList = NodeList()
	ctx = zmq.Context()
	cmd_receiver = ctx.socket(zmq.PULL)
	cmd_receiver.bind(nodeList.get_node('cmd_in'))
	cmd_sender = ctx.socket(zmq.PUSH)
	cmd_sender.bind(nodeList.get_node('cmd_out'))

	while True:

		try:	
			cmd_message = cmd_receiver.recv(zmq.NOBLOCK)
			print(cmd_message)
		except zmq.ZMQError, e:
			pass


		time.sleep(1)
			
if __name__ == "__main__":
    main = main()