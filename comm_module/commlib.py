import zmq
import random
import time
import socket
import node_list as nl


"""
Set up sockets
"""
tele_sock = socket.socket(	socket.AF_INET, # Internet
							socket.SOCK_DGRAM) # UDP

ctx = zmq.Context()
groundstation_sender = ctx.socket(zmq.PUSH)
groundstation_sender.connect(nl.get_address('cmd_in'))

"""
Communication functions
"""
def sendTelemetry(args=[]):
	"""
	UDP Sends telemetry message to groundstation
	"""
	MESSAGE = "%s: %s" % (time.time(), ", ".join(args))
	tele_sock.sendto(MESSAGE, (nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2])) # [0]: address, [1]: port

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