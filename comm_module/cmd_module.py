from datetime import datetime
import random
import time
import zmq
import sys
import os
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
	
	print_out("============================")
	print_out("=====  Command module  =====")
	print_out("============================")
	print_out("")

	while True:
		try:	
			cmd_message = cmd_receiver.recv(zmq.NOBLOCK)
			if (cmd_message != ""):
				print_out("Command received")
				if (cmd_message == 'control_brake'):
					print_out(cmd_message)
					# action controlled brake function
				elif (cmd_message == 'safe_brake'):
					print_out(cmd_message)
					# action safe brake function
				elif (cmd_message == 'aux_speed'):
					print_out(cmd_message)
					# set auxilliary speed function
				elif (cmd_message == 'aux_turn'):
					print_out(cmd_message)
					# turn the pod using auxilliary propulsion function (might not be possible)
				elif (cmd_message == 'dump_log'):
					print_out("Dumping log to file...")

					# get stuff from datastore?
					data = ["log file start\n",
							"data: %s\n"%random.random(),
							"data 2: %s\n"%random.random(),
							"data 3: %s\n"%random.random()]

					filename = str(datetime.now()).split(".")[0].replace(" ","_").replace(":","-")
					f = open("%s.txt"%filename, "w")
					for line in data:
						f.write(line)
					f.close()
					print_out("Done.")

				elif (cmd_message == 'update_firmware'):
					print_out(cmd_message)
					# update teensy firmware function
				else:
					print_out("Command not found: %s"%cmd_message)

		except zmq.ZMQError, e:
			pass

		time.sleep(1)
			
if __name__ == "__main__":
    main = main()
