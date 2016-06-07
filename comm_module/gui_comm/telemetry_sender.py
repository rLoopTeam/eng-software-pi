from datetime import datetime
import threading
import random
import json
import time
import zmq
import sys
import node_list as nl
import commlib as comm

def print_out ( str ):
	sys.stdout.write( str )
	sys.stdout.write( "\n" )
	sys.stdout.flush()

def nextState (_state):
	return {
		1: (_state[1] + 1) % 500,
		3: _state[3] + (random.random() - 0.5),
		11: _state[11] + (random.random() - 0.5)/10,
		55: (_state[55] + 4.1) % 500
	}

print_out("============================")
print_out("===== Telemetry sender =====")
print_out("============================")
print_out("")

state = {
  1: 0, # seq
  3: 30, # temp
  11: 8, # current
  55: 0 # speed
}

while True:
	message = {
		"node": "command",
		"data": [1, state[1], 3, state[3], 11, state[11], 55, state[55]],
		"mts": str(datetime.now())
	}
	print_out('telemetry' + ' ' + json.dumps(message))	
	state = nextState(state)
	comm.sendTelemetry('telemetry' + ' ' + json.dumps(message))
	time.sleep(1/5)

