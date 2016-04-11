import zmq
import psycopg2
#for testing
from datetime import datetime

#####OPTIONS############
module_in = "ipc://module_i2c"
db_name = "rLoop"
db_user = "peter"
########################

#SOCKET

context = zmq.Context()
#this is a subscriber socket
receiver = context.socket(zmq.SUB)

###MISSING: exception handling!
receiver.connect(module_in)
# subscribe!
receiver.setsockopt(zmq.SUBSCRIBE,"")


#DATABASE

###MISSING: exception handling!
db_con =  psycopg2.connect("dbname=%s user=%s" % (db_name, db_user))
db_cursor = db_con.cursor()


#MAIN LOOP
'''
while True:
	#TEST: creating random data
	sid = 10
	aid = 2
	timestamp = datetime.utcnow()
	value = float(1234)
	#get Data from i2c module
###MISSING: data format we are getting...
	try:
		buf = receiver.recv()
		print buf
	except KeyboardInterrupt:
		break
	#store it in the database somehow
###MISSING: which table do we write to? Is this decided here or do we write to the same table every time? In this case put a variable in the "OPTIONS" section
	# db_cursor.execute("""INSERT INTO Data VALUES (%s, %s, %s, %s);""",(sid, aid, timestamp, value))
	#commit the changes
	# db_con.commit()
'''
#testing
sid = 1
aid = 1
timestamp = datetime.utcnow()
value = float(0.05)
db_cursor.execute("""INSERT INTO Data VALUES (%s, %s, %s, %s);""",(sid, aid, timestamp, value))
db_con.commit()
#this should be executed when the program is stopped
#terminate db connection
db_cursor.close()
db_con.close()
#terminate socket
receiver.close()
context.term()
