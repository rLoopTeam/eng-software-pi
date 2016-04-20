//Written by Peter S. Gschladt (psg1337) for rLoop
//general includes
#include <iostream>

//zmq includes
#include "zhelpers.hpp" 	//zmq helper header for c++, written by zmq themselves. Will create our own header later

//i2c includes
#include <sys/ioctl.h>
#include <fcntl.h>
#include "i2c_recvbin.h"	//header for i2c functions
#include "bsc-slave.h"		//i2c slave header

//zmq defines
#define PROCADDR 	"ipc://module_i2c" //address this module binds to
#define CMDPROCADDR 	"ipc://module_cmd" //address the command module is bound to

//i2c defines
#define SLV_ADDR  	 0x33


//function for sending the frame retrieved over i2c
bool sendframe(zmq::socket_t & socket, const unsigned char* const buffer, int size) {
	try {
		zmq::message_t message(size+1);
		memcpy (message.data(), buffer, size+1);
		bool bytessent = socket.send(message);
		return bytessent;
	}
	catch (zmq::error_t e) {
	//MISSING: investigate if EAGAIN throw is caught by language binding
			std::cout << "ERROR while sending: " << zmq_strerror(e.num()) << std::endl;
			return false;
	}
}

int main(){
	//signal catcher from zhelpers.hpp
	s_catch_signals();
	
	int i2c_fd; 				//i2c filedescriptor
	const int maxbytes = 512;		//maximum count of bytes received from i2c
	unsigned char buffer[maxbytes];		//our buffer
	int bytecount;				//how many bytes we have received from i2c
	
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
	if((i2c_fd = open("testframe.txt", O_RDONLY)) == -1){
		std::cout << "error while trying to open file" << std::endl;
		return -1;
	}
	
// MAIN LOOP
	while(1){
		//if an interrupt is detected, break the loop /pun intended
		if(s_interrupted){
			break;
		}
		bool rc;
		bytecount = 0;
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
		if((bytecount = i2c_frametobufbin(i2c_fd, buffer, maxbytes)) <= 0){
			if(bytecount == 0) std::cout << "No bytes received" << std::endl;
			else std::cout << "Error while reading from file" << std::endl;
			continue;
		}
		//TEST:
		std::cout << "Frame content in hex:" << std::endl;
		for(int i=0;i<bytecount;i++){
			printf("%x ",buffer[i]);
		}
		std::cout << std::endl;
		sleep(5);
		//END TEST
		sendframe(dbsender, buffer, bytecount);
	}
	close(i2c_fd);
	//close() and destroy() of zmq are handled by destructors in language binding
	return 0;
}
