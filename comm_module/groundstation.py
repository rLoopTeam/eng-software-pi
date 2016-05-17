#from matplotlib import style
from matplotlib.figure import Figure
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import ttk
import tkMessageBox
import threading
import random
import socket
import time
import zmq
import sys
import node_list as nl
import commlib as comm
import matplotlib.animation as animation
import matplotlib.pyplot as plt

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
	if bool(re.compile('^[a-z0-9\._]+$').match(cmd)):
		comm.sendCommand([cmd]) # comm library which has takes care of all the sockets for you
		print_out("Command sent: %s"%cmd)
	else:
		tkMessageBox.showwarning("Wrong syntax", "You can only send commands made of letters and numbers")

"""
GUI
"""
def redCircle():
    circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='red')
    colorLog.insert(0.0, "Red\n")

def yelCircle():
    circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='yellow')
    colorLog.insert(0.0, "Yellow\n")

def grnCircle():
    circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='green')
    colorLog.insert(0.0, "Green\n")

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

window.wm_title('rLoop groundstation')
window.geometry('900x500+500+300')
window.resizable(width=FALSE, height=FALSE)

leftFrame = Frame(window, width=200, height = 500)
leftFrame.grid(row=0, column=0, padx=10, pady=2)
rightFrame = Frame(window, width=300, height = 500)
rightFrame.grid(row=0, column=1, padx=10, pady=2)

title_label = Label(leftFrame, text="Stats").grid(row=0, column=0, padx=10, pady=2)

Instruct = Label(leftFrame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
Instruct.grid(row=1, column=0, padx=10, pady=2)

try:
    imageEx = PhotoImage(file = 'image.gif')
    Label(leftFrame, image=imageEx).grid(row=2, column=0, padx=10, pady=2)
except:
    print("Image not found")
    
#Right Frame and its contents
rightFrame = Frame(window, width=400, height = 600)
rightFrame.grid(row=0, column=1, padx=10, pady=2)

circleCanvas = Canvas(rightFrame, width=100, height=100, bg='white')
circleCanvas.grid(row=0, column=0, padx=10, pady=2)

btnFrame = Frame(rightFrame, width=200, height = 200)
btnFrame.grid(row=1, column=0, padx=10, pady=2)

colorLog = Text(rightFrame, width = 30, height = 10, takefocus=0)
colorLog.grid(row=2, column=0, padx=10, pady=2)

redBtn = Button(btnFrame, text="Red", command=redCircle)
redBtn.grid(row=0, column=0, padx=10, pady=2)

yellowBtn = Button(btnFrame, text="Yellow", command=yelCircle)
yellowBtn.grid(row=0, column=1, padx=10, pady=2)

greenBtn = Button(btnFrame, text="Green", command=grnCircle)
greenBtn.grid(row=0, column=2, padx=10, pady=2)

cmd_label = Label(leftFrame, text="Command")
cmd_label.grid(row=0, column=1, sticky=W)
cmd_entry = Entry(leftFrame, textvariable=command_entry)
cmd_entry.grid(row=0, column=2, sticky=W)


cmd_button = Button(leftFrame, text="Send", command = lambda: send_command(command_entry))
cmd_button.grid(row=0, column=3, sticky=W)

cmd_entry.focus() # set focus on entry field

# plot graphs.
# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = arange(0.0, 3.0, 0.01)
# s = sin(2*pi*t)
# a.plot([1,2,3,4,5], [1,2,3,4,2])

# canvas = FigureCanvasTkAgg(f, master=window)
# canvas.show()
# canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

# canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)


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