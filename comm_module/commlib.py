import zmq
import random
import time
import socket
import node_list as nl

def sendTelemetry(args=[]):
		"""
		UDP Sends telemetry message to groundstation
		"""
		MESSAGE = "[timestamp] %s" % (", ".join(args))
		sock = socket.socket(	socket.AF_INET, # Internet
								socket.SOCK_DGRAM) # UDP
		sock.sendto(MESSAGE, (nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2])) # [0]: address, [1]: port
		sock.close()


# class Communication():
	
# 	#nodeList = NodeList()

# 	def sendTelemetry(self, args):
# 		"""
# 		UDP Sends telemetry message to groundstation
# 		"""
# 		MESSAGE = "[timestamp] %s" % random.random
# 		sock = socket.socket(	socket.AF_INET, # Internet
# 								socket.SOCK_DGRAM) # UDP
# 		sock.sendto(MESSAGE, (self.nodeList.get_node_as_tuple('gs_in')[1], self.nodeList.get_node_as_tuple('gs_in')[2]))

# 		# ctx = zmq.Context()
# 		# s = ctx.socket(zmq.PUSH)
# 		# s.bind(self.nodeList.get_node_as_tuple('gs_in'))
# 		# se.send(args[0])



