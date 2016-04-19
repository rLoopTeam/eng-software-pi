import socket
import zmq
import sys
import time
import node_list as nl

def print_out ( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

def main():
	
	ctx = zmq.Context()

	"""
	UDP telemetry receiver socket
	"""
	groundstation_receiver = socket.socket(	socket.AF_INET, # Internet
	                     					socket.SOCK_DGRAM) # UDP
	groundstation_receiver.bind((nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2]))

	"""
	TCP commander sender/receiver socket
	"""
	# groundstation_sender = ctx.socket(zmq.PUSH)
	# groundstation_sender.bind(nl.get_address('gs_out'))

	while True:
		# command = "MOVE_FORWARD"
		# groundstation_sender.send(command)
		# print_out("GS: COMMAND: %s"%command)
	
		message, addr = groundstation_receiver.recvfrom(1024) # buffer size is 1024 bytes
		print_out("GS: TELEMETRY: %s"%message)

		time.sleep(2)


if __name__ == '__main__':
	main()