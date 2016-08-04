import zmq
import time

#Set database to use
database = "sqlite3"

#####OPTIONS############
module_in = "ipc://module_i2c"
db_name = "rLoop"
db_user = "rloop" #rloop - DY
########################

#####
#Sensor Identity 
SensorName='TestSens'

#CONCEPT: Store attribute listing and handle all the info on python prior to DB insertion
#Attribute = ["Test1", "Test2", "Test3"] #AttributeNames

#####
#GLOBAL SWITCH
ZMQActive = 0
DBACTIVE = 0

#SOCKET

context = zmq.Context()
#this is a subscriber socket
receiver = context.socket(zmq.SUB)

while(1):
    try:
       #Nothing can really be done when receiver is gone
       #Can only tell base station that receiver connection has failed
       receiver.connect(module_in)
       ZMQActive = 1
       break

    except:
       print "Receiver connection failed"

       #Perhaps forward this information to base station via a different protocol?
       #GSM, ICMP, BPSK-DSSS,...
       time.sleep(1) 
       #Wait 1 second for reconnect

# Please give a thumbs up, like and subscribe to my ZMQ socket!
receiver.setsockopt(zmq.SUBSCRIBE,"")


#DATABASE
#Add pytime with the sql NOW() in case DB dies for caching

QueryCache = []

while 1:
    try:
    	db_con = ""
	if database == "postgres":
	   import postgres 
           db_con = psycopg2.connect("dbname=%s user=%s" % (db_name, db_user))
	else:
	   import sqlite3 
	   db_con = sqlite3.connect('LocalPod.db')
        db_cursor = db_con.cursor()
        DBACTIVE = 1
    except:
        print "Postgres is down, connection failed"

        if(ZMQActive):

            #Implement a loop here to continuous capture data from ZMQ but save it in a cache, either Local Redis or Postgres
            CacheTS = time.time()
            value = float(1234)
            #Need to get data from i2c via ZMQ
            QueryCache.append("""INSERT INTO Data VALUES (select sid from Sensors where SensorName = {SensName}, select aid from Attributes where AttrName = {AttrName}, {TimeStamp},{DataVal} );""",(SensName = SensorName, AttrName = Attribute, TimeStamp = CacheTS, DataVal = value))

#Submit all the uninserted queries during DB recovery
for i in QueryCache:
   db_cursor.execute(i)

while 1:
	try:
            buf = receiver.recv()
            print buf
	except KeyboardInterrupt:
            break

	#store it in the database somehow
###MISSING: which table do we write to? Is this decided here or do we write to the same table every time? In this case put a variable in the "OPTIONS" section

        Attribute='TestA'
        value = float(1234)
	CurrentTS = time.time()
        db_cursor.execute("""INSERT INTO Data VALUES (select sid from Sensors where SensorName = {SensName}, select aid from Attributes where AttrName = {AttrName}, {TimeStamp},{DataVal} );""",(SensName = SensorName, AttrName = Attribute, TimeStampe = CurrentTS, DataVal = value))
	db_con.commit()

#terminate db connection
db_cursor.close()
db_con.close()
#terminate socket
receiver.close()
context.term()
