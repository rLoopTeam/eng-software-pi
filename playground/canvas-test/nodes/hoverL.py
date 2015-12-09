import time
import canvas
from IDs import MessageList as ml

receive_message_ids = [# receive: get engine status, tilt engine, stop engine # low level commands
			ml.messages['get_engine_status_l']['id'],
			ml.messages['tilt_l']['id'],
			ml.messages['stop_l']['id'],
			ml.messages['start_l']['id']] 

def main():
	receiver = canvas.init_receiver()
	sender = canvas.init_sender()
	time.sleep(0.5) #sleep to allow for canvas server startup. horrible hack that will go away soon
		
	#add message id filters on receiver
	canvas.add_id(receiver, receive_message_ids)
	canvas.print_out("HOVER ENGINE L started")
	canvas.print_out("Hover L node started")
	canvas.print_out("Reset engine L tilt")
	
	# default state of engine
	enabled = False
	tilt = 0
	
	while 1:
		#receive message from CAN bus (only returns messages that this node has subscribed to)
		#this call will block untill a message is received
		msg_id, msg_data = canvas.recv(receiver)
		
		if (msg_id == ml.messages['get_engine_status_l']['id']):
			status = 'Engine L is chill. Enabled: %s, Tilt: %s' % (enabled, tilt)
			canvas.print_out("Hover engine status L: %s" % status)
			canvas.send(sender, ml.messages['engine_status_l']['id'], status)
			
			# add other engines here...
			
		elif (msg_id == ml.messages['tilt_l']['id']):
			canvas.print_out("Tilt engine L %s degrees" % msg_data)
			
			# set engine L tilt
			tilt = msg_data
			
			# return engine L status after setting the tilt
			status = 'Tilt L status: Enabled: %s, Tilt: %s' % (enabled, tilt)
			canvas.send(sender, ml.messages['engine_status_l']['id'], status)
		
		elif (msg_id == ml.messages['start_l']['id']):
			canvas.print_out("Start engine L")
			enabled = True
			
			# return engine L status after starting
			status = 'Start L status: Enabled: %s, Tilt: %s' % (enabled, tilt)
			canvas.send(sender, ml.messages['engine_status_l']['id'], status)
			
		elif (msg_id == ml.messages['stop_l']['id']):
			canvas.print_out("Stop engine L")
			enabled = False
			
			# return engine L status after stopping
			status = 'Stop L status: Enabled: %s, Tilt: %s' % (enabled, tilt)
			canvas.send(sender, ml.messages['engine_status_l']['id'], status)

		#sleep node for 1 second
		time.sleep(1)

if __name__ == '__main__':
    main()
