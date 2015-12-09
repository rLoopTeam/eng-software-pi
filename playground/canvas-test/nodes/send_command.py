import sys
import time
import canvas
from IDs import MessageList as ml

def main():
	sender = canvas.init_sender()
	print(sys.argv)
	
	no_args = len(sys.argv)
	
	if no_args > 1:
		if sys.argv[1] in ml.messages:
			message_id = ml.messages[sys.argv[1]]['id']
			message_data = ''
			
			if 'input_data' in ml.messages[sys.argv[1]]:
				if no_args == 3:
					print("Input data given. Sending command...")
					message_data = sys.argv[2]
					canvas.send(sender, message_id, message_data)
				else:
					print("Input data required but not given. Aborted.")
			else:
				print('No input data allowed. Sending command...')
				canvas.send(sender, message_id, message_data)

		else:
			print("Command not found")
	else:
		print('Please provide a command')

if __name__ == '__main__':
    main()
