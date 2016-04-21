import zmq
import random
import time
import threading
import node_list as nl
import commlib as comm

while True:
	comm.sendTelemetry(["Sup"])