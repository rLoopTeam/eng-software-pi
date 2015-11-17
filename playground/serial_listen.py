import serial as serial

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
#port.open()
print("Python -  Send message")
print("======================")
port.write("Hello Teensy! This is Python, do you hear me? \n")

while True:
	rcv = port.read(size=250)
	if (rcv != ""):
		print(rcv)