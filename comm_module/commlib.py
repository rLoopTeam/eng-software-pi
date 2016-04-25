import zmq
import random
import time
import socket
import node_list as nl

def sendTelemetry(args=[]):
		"""
		UDP Sends telemetry message to groundstation
		"""
		MESSAGE = "%s: %s" % (time.time(), ", ".join(args))
		sock = socket.socket(	socket.AF_INET, # Internet
								socket.SOCK_DGRAM) # UDP
		sock.sendto(MESSAGE, (nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2])) # [0]: address, [1]: port
		sock.close()

