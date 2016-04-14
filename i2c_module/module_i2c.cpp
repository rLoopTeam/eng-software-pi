//Written by Peter S. Gschladt (psg1337) for rLoop
//general includes
#include <iostream>

//zmq includes
#include "zhelpers.hpp" 	//zmq helper header for c++, written by zmq themselves. Will create our own header later

//i2c includes
#include <sys/ioctl.h>
#include <fcntl.h>
#include "i2c_recv.h"		//header for i2c functions
#include "bsc-slave.h"		//i2c slave header

//zmq defines
#define PROCADDR 	"ipc://module_i2c" //address this module binds to
#define CMDPROCADDR 	"ipc://module_cmd" //address the command module is bound to

//i2c defines
#define SLV_ADDR  	 0x33


//function for sending a specified string out on a specified socket
void send(zmq::socket_t &sender, std::string &buffer){
	try {
		s_send(sender, buffer);
	}
	catch (zmq::error_t e) {
//MISSING: investigate if EAGAIN throw is caught by language binding
		std::cout << "ERROR while sending: " << zmq_strerror(e.num()) << std::endl;
	}
}

int main(){
	//signal catcher from zhelpers.hpp
	s_catch_signals();
	
	int i2c_fd; 			//i2c filedescriptor
	std::string buffer;		//our buffer
	const int maxbytes = 50;	//maximum count of bytes received from i2c
	int bytecount;			//how many bytes we have received from i2c
	
// SOCKETS
	//create zmq context
	zmq::context_t context(1);
	
	//create the socket for sending telemetry to db
	zmq::socket_t dbsender(context, ZMQ_PUB);
	try {
		dbsender.bind(PROCADDR);
	} catch (zmq::error_t e) {
		std::cout << "ERROR on bind." << zmq_strerror(e.num()) << std::endl;
		return -1;
	}
	//create listener socket for incoming commands from the GS
	zmq::socket_t cmdlistener(context, ZMQ_PAIR); //to be decided, which Socket type is best
	try {
		cmdlistener.connect(CMDPROCADDR);
	} catch (zmq::error_t e) {
		std::cout << "ERROR on connect to command module" << zmq_strerror(e.num()) << std::endl;
		return -2;
	}
//I2C init
	//open the i2c slave
	/* TEST: commented out
	if((i2c_fd = open("/dev/i2c-slave", O_RDWR)) == -1){
   		std::cout << "ERROR on opening i2c-slave" << std::endl;
 	}
 	//set the i2c slave address
 	if( (ioctl(i2c_fd, I2C_SLAVE, SLV_ADDR) < 0) ){
		std::cout << "ERROR on setting the i2c slave address. QUIT" << std::endl;
	    	return -1;
  	}
  	*/
  	//TEST: initialize the i2c file descriptor to read from a test file
	if((i2c_fd = open("test.txt", O_RDONLY)) == -1){
		std::cout << "error while trying to open file" << std::endl;
		return -1;
	}
	
// MAIN LOOP
	while(1){
		bool rc;
		//prioritize incoming commands from command process
		/* COMMENTED OUT since command module isn't functional yet.
		do{
			zmq::message_t command;
			try {
				rc = cmdlistener.recv(&command, ZMQ_DONTWAIT);
			} catch (zmq::error_t e) {
				std::cout << "ERROR while receiving from command module:" << zmq_strerror(e.num()) << std::endl;
				//set rc to false, so the if statement doesnt try anything funny
				rc = false;
			}
			if(rc == true){
				//MISSING: send command to Teensy via i²c
			}
		} while(rc == true);
		*/
		//receive telemetry from teensy and push it out to the db, one frame at a time
		if((bytecount = i2c_getframestr(i2c_fd, buffer, maxbytes)) <= 0){
			std::cout << "Error while reading from file" << std::endl;
			continue;
		}
	//MISSING: reformat data before sending it
		//TEST:
		std::cout << buffer  << std::endl;
		sleep(1);
		//END TEST
		send(dbsender, buffer);
		//if an interrupt is detected, break the loop /pun intended
		if(s_interrupted){
			break;
		}
	}
	close(i2c_fd);
	//close() and destroy() of zmq are handled by destructors in language binding
	return 0;
}
