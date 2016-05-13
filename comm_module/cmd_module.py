from datetime import datetime
import subprocess
import settings
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

def update_teensy_firmware():
	try:
		ret = subprocess.call(["sudo -S python %sautoLoader.py %sremote.hex"%(settings.autoloader_script_location, settings.hex_location)])
	except OSError:
		ret = "Cannot run this command on windows. Or the script/hex might be missing"
	return ret

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
				if (cmd_message == 'control_brake'): # action controlled brake function
					print_out(cmd_message)
					
				elif (cmd_message == 'safe_brake'): # action safe brake function
					print_out(cmd_message)
					
				elif (cmd_message == 'aux_speed'): # set auxilliary speed function
					print_out(cmd_message)
					
				elif (cmd_message == 'aux_turn'): # turn the pod using auxilliary propulsion function (might not be possible)
					print_out(cmd_message)
					
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

				elif (cmd_message == 'update_teensy_firmware'): # update teensy firmware function
					print_out("Flashing Teensy...")
					res = update_teensy_firmware()
					print_out(res)

				else:
					print_out("Command not found: %s"%cmd_message)

		except zmq.ZMQError, e:
			pass

		time.sleep(1)
		

if __name__ == "__main__":
    main = main()
