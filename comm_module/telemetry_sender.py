import threading
import random
import time
import zmq
import sys
import node_list as nl
import commlib as comm

def print_out ( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

print_out("============================")
print_out("===== Telemetry sender =====")
print_out("============================")
print_out("")

while True:
	message = "temp: %s, pressure: %s"%(random.random(), random.random())
	print_out("Telemetry sent: %s"%message)	
	comm.sendTelemetry([message])
	time.sleep(1)
