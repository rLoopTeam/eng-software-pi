from datetime import datetime
import random
import struct
import time
import json
import zmq
import os
import sys

#########################################
######TODO:
######PROPERLY HANDLE ESCAPED DATA
#########################################

def checkChecksum(prevBytes, checksum):
	checksum = struct.unpack("B",checksum)[0]
	a = 0
	prevBytes = [struct.unpack("B",b)[0] for b in prevBytes]
	for b in prevBytes:
		a ^= b
	return (a == checksum)

"""
Sockets and i2c setup
"""
port = "/dev/i2c-slave"

ctx = zmq.Context()
tele_sock = ctx.socket(zmq.PUB)
tele_sock.bind("tcp://*:3000")

"""
Variables
"""
prevbyte = None
prevBytes = []
isHeader = False
isParam = False
index = 0
frame_length_low = None 
frame_length_high = None 
header_buff = []
param_buff = bytearray()
param_length = 0
param_type = None
parameters = []
lastWasControlChar = False
lastId = -1
lastIndex = 0

message = {
	"node": "command",
	"data": [],
	"mts": None
}

fd = open(port, "rb")

while True:

	bytes = fd.read(100) 
	
	for byte in bytes:
		if byte == '\xd5' and lastWasControlChar == False:
			lastWasControlChar = True
		else:
			if lastWasControlChar == True and byte == '\xd5':
				prevBytes.append('\xd5')
				print "Escaped byte!"
		
			#Need to tweak this in case a control character follows an escaped character
			#or there are multiple escaped data characters in a row
			if lastWasControlChar == True and byte != '\xd5':
				if (len(param_buff) > param_length):
					print(len(param_buff), param_length, param_type)
					print("ERROR: Number of bytes in parameter is great than the length defined in the header. Data may be corrupt")
					header_buff = []
					isHeader = False
					isParam = False
					#break 
					#There will almost always be an error when it starts reading
					#due to stuff stuck in the device buffer

				elif (len(param_buff) != 0 and param_length != 0 and len(param_buff) == param_length): #when we reached the final byte
					#print "PROC"
					"""
					0 - Raw byte string
					1 - Signed Integer
					2 - Unsigned Integer
					3 - Floating Type
					"""

					# Raw byte stream not implemented in Teensy I2C library yet
					
					#Signed 8-bit integer
					if (param_type == 1 and param_length == 1):
						message['data'].append(struct.unpack_from("!b", param_buff)[0])

					#Unsigned 8-bit integer
					if (param_type == 2 and param_length == 1):
						message['data'].append(struct.unpack_from("!B", param_buff)[0])

					#Signed 16-bit integer
					if (param_type == 1 and param_length == 2):
						message['data'].append(struct.unpack_from("!h", param_buff)[0])

					#Unsigned 16-bit integer
					if (param_type == 2 and param_length == 2):
						message['data'].append(struct.unpack_from("!H", param_buff)[0])
					
					#Signed 32-bit integer
					if (param_type == 1 and param_length == 4):
						message['data'].append(struct.unpack_from("!i", param_buff)[0])
						if lastId == 50:
							#print str(struct.unpack_from("!i", param_buff)[0])
							if  struct.unpack_from("!i", param_buff)[0] != (lastIndex+1):
								print "Jump from "+str(lastIndex)+" to "+ str(struct.unpack_from("!i", param_buff)[0])
							lastIndex =  struct.unpack_from("!i", param_buff)[0]

					#Unsigned 32-bit integer
					if (param_type == 2 and param_length == 4):
						message['data'].append(struct.unpack_from("!I", param_buff)[0])
						
					#Signed 64-bit integer
					if (param_type == 1 and param_length == 8):
						message['data'].append(struct.unpack_from("!q", param_buff)[0])

					#Unsigned 64-bit integer
					if (param_type == 2 and param_length == 8):
						message['data'].append(struct.unpack_from("!Q", param_buff)[0])	

					#32-bit floating Point
					if (param_type == 3 and param_length == 4):
						message['data'].append(struct.unpack_from("!f", param_buff)[0])

					#64-bit floating Point
					if (param_type == 3 and param_length == 8):
						message['data'].append(struct.unpack_from("!d", param_buff)[0])
						
				header_buff = []
				header_buff.append("\xd5")
				param_buff = bytearray()
				isHeader = True

			if (isHeader == True):
				header_buff.append(byte)
				
				if len(header_buff) > 4:
					#something is not right, reset until the next control character
					header_buff = []
					isHeader = False
					isParam = False

				if len(header_buff) == 4:
					if header_buff[1] == '\xd0': # START of FRAME
						#print "SOF"
						frame_length_high = header_buff[2]
						frame_length_low = header_buff[3]
						prevBytes = []
						message['data'] = []
						prevBytes.append(header_buff[0])
						prevBytes.append(header_buff[1])
						prevBytes.append(header_buff[2])
						prevBytes.append(header_buff[3])
						isParam = True

					elif header_buff[1] == '\xd3': # START of PARAMETER
						#print "SOP"
						param_length = (struct.unpack("B",header_buff[2])[0]&0xF0) >> 4 
						param_type = struct.unpack("B",header_buff[2])[0]&0x0F
						prevBytes.append(header_buff[0])
						prevBytes.append(header_buff[1])
						prevBytes.append(header_buff[2])
						prevBytes.append(header_buff[3])
						message['data'].append(struct.unpack("B",header_buff[3])[0]) # add parameter id to message
						lastId = struct.unpack("B",header_buff[3])[0] 
						param_buff = bytearray()

					elif header_buff[1] == '\xd8': # END of FRAME
						#print "--EOF"
						#This frame data isn't used in the checksum
						#(it'd create a circular dependency)
						checksum = header_buff[2]
						if (checkChecksum(prevBytes, checksum) == False): # calculate checksum to see if frame is valid
							print "Checksum error"
							#print prevBytes
							message['data'] = [] # clear message because it is corrupted
						else:
							message['mts'] = str(datetime.now()) # timestamp
							data = json.dumps(message)
							data = "telemetry " + data
							tele_sock.send( data)
						isParam = False

					isHeader = False
					
			elif (isHeader == False and isParam == True):
				param_buff.append(byte)
				prevBytes.append(byte)

			prevbyte = byte # lagging var
			lastWasControlChar = False
