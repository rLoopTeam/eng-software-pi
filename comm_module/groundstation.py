from Tkinter import *
import tkMessageBox
import threading
import socket
import zmq
import sys
import time
import node_list as nl

"""
Setup variables and helper functions
"""
#- Helper functions
def print_out( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

def send_command(entryvar):
	cmd = entryvar.get()
	if bool(re.compile('^[a-z0-9\.]+$').match(cmd)):
		groundstation_sender.send(cmd, zmq.NOBLOCK)
		print_out("Command sent: %s"%cmd)
	else:
		tkMessageBox.showwarning("Wrong syntax", "You can only send commands made of letters and numbers")

"""
zmq
"""
ctx = zmq.Context()

"""
Communication - setup sockets and define comm_loop
"""
#- UDP telemetry receiver socket
groundstation_receiver = socket.socket(	socket.AF_INET, # Internet
										socket.SOCK_DGRAM) # UDP
groundstation_receiver.bind((nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2]))
groundstation_receiver.setblocking(0)

#- TCP commander sender/receiver socket
groundstation_sender = ctx.socket(zmq.PUSH)
groundstation_sender.connect(nl.get_address('cmd_in'))

def comm_loop():
	while True:
		print_out("receive")
		"""
		Receive telemetry
		"""
		try:
			message = groundstation_receiver.recv(zmq.NOBLOCK) # buffer size is 1024 bytes
			if message:
				print_out("GS: TELEMETRY: %s"%message)
		except:
			pass
		time.sleep(1)

#- Create separate separate thread for the communication process for improved performance. 
#- GUI seems to cause massive performance loss without this
thread = threading.Thread(target=comm_loop)
thread.daemon = True 
thread.start()

"""
GUI
"""
window = Tk()
command_entry = StringVar()

window.geometry('350x50+500+300')
window.title('rLoop groundstation')

cmd_label = Label(window, text="Command")
cmd_label.grid(row=0, column=1, sticky=W)

cmd_entry = Entry(window, textvariable=command_entry)
cmd_entry.grid(row=0, column=2, sticky=W)

cmd_button = Button(window, text="Send", command = lambda: send_command(command_entry))
cmd_button.grid(row=0, column=3, sticky=W)

cmd_entry.focus() # set focus on entry field
window.mainloop()


"""
Cleanup. !Not sure if needed!
"""
groundstation_receiver.close() # not sure where to stick this
groundstation_sender.close()
		
	

"""
Initialisation
"""
if __name__ == '__main__':
	pass