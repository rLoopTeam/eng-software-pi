from Tkinter import *
import tkMessageBox
import threading
import socket
import time
import zmq
import sys
import node_list as nl
import commlib as comm

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
		comm.sendCommand([cmd]) # comm library which has takes care of all the sockets for you
		print_out("Command sent: %s"%cmd)
	else:
		tkMessageBox.showwarning("Wrong syntax", "You can only send commands made of letters and numbers")

"""
Communication - setup sockets and define comm_loop
"""
#- UDP telemetry receiver socket
groundstation_receiver = socket.socket(	socket.AF_INET, # Internet
										socket.SOCK_DGRAM) # UDP
groundstation_receiver.bind((nl.get_address_as_tuple('gs_in')[1], nl.get_address_as_tuple('gs_in')[2]))
groundstation_receiver.setblocking(0)

print_out("=============================")
print_out("=====   Groundstation   =====")
print_out("=============================")
print_out("")

def comm_loop():
	buff = 1024
	while True:
		"""
		Receive telemetry
		"""
		try:
			message = groundstation_receiver.recv(buff) # buffer size is 1024 bytes
			if message:
				print_out(message)
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
	

"""
Initialisation
"""
if __name__ == '__main__':
	pass