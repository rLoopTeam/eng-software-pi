#ifndef __I2CRECV_INCLUDED
#define __I2CRECV_INCLUDED

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <iostream>

//not used atm
//#define I2C_SEPARATOR 	0x20	//separator for values in the stream

//read from filedescriptor
int i2c_frametobuf(int &fd, char* const buffer, int buf_size){
	int bytecount=0;
	bool soframe = false;
	//fill the passed buffer with separators
	memset(buffer, 0x00, buf_size);
	while(1){
		char byte[1];
		if(read(fd, byte, 1) == -1){
	     		printf("unable to read!\n after %i bytes", bytecount);
	     		//return a value that tells us something has gone wrong and at which point
	     		return -1-bytecount;
	  	}
	  	//detect start of frame
  		if((*byte == 0x02) && !soframe){
  			soframe = true;
  			printf("start of frame\n");
  			continue;
  		}
  		//detect end of frame
  		if((*byte == 0x00) && soframe){
  			printf("end of frame\n");
  			break;
  		}
  		//write the byte into buffer as long as the passed buffer has space for us
  		if(soframe && (bytecount<buf_size)){
  			buffer[bytecount] = *byte;
  			bytecount++;
  		} else {
  			//make the bytecount bigger than the size of the buffer
  			bytecount++;
  			break;
  		}
  	}
	return bytecount;
}

//use i2c_frametobuf to read from filedescriptor to buffer and then put the stuff that was read into a string
int i2c_getframestr(int &fd, std::string &str, int maxbytes){
	int bytecount;
	char buffer[maxbytes];
	if((bytecount = i2c_frametobuf(fd, &(*buffer), sizeof(buffer))) < 0){
			return -1;
	}
	//put all that received stuff into the passed string
	str = static_cast<std::string>(buffer).substr(0,bytecount);
	if(bytecount > maxbytes){
		return -2;
	}
	return bytecount;
}

#endif
