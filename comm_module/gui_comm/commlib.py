import zmq
import random
import time
import socket
import node_list as nl


"""
Set up sockets
"""
ctx = zmq.Context()

# tele_sock = socket.socket(	socket.AF_INET, # Internet
# 							socket.SOCK_DGRAM) # UDP
tele_sock = ctx.socket(zmq.PUB)
tele_sock.bind("tcp://%s:%s"%(nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2]))

groundstation_sender = ctx.socket(zmq.PUSH)
groundstation_sender.connect(nl.get_address('cmd_in'))

"""
Communication functions
"""
def sendTelemetry(msg):
	"""
	UDP Sends telemetry message to groundstation
	"""
	#tele_sock.sendto(msg, (nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2])) # [0]: address, [1]: port
	tele_sock.send(msg) # [0]: address, [1]: port

def sendCommand(args=[]):
	MESSAGE = ", ".join(args)
	groundstation_sender.send(MESSAGE , zmq.NOBLOCK)

def cleanUp():
	tele_sock.close()
	groundstation_sender.close()

"""
Initialisation
"""
if __name__ == '__main__':
	pass