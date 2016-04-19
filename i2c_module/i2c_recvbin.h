//Written by Peter S. Gschladt (psg1337) for rLoop
#ifndef __I2CRECVBIN_INCLUDED
#define __I2CRECVBIN_INCLUDED

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <iostream>
#include <netinet/in.h>		//for ntohs()

#define I2C_ESCAPE 	0xD5	//escape character in the stream
#define I2C_SOFRAME	0xD0	//start of frame character
#define I2C_PARAMDELIM	0xD3	//parameter delimiter character
#define I2C_EOFRAME	0xD8	//end of frame character
#define MAX_WAIT	512	//maximum number of tries to find a I2C_SOFRAME


//get checksum from the frame
uint8_t getchecksum(const unsigned char* const buffer, uint16_t length){
	return buffer[length-2];
}

//compute checksum
uint8_t computechecksum(const unsigned char* const buffer, uint16_t length){
	uint8_t checksum = 0;
	for(uint16_t i=0;i<length-4;i++){
		checksum ^= buffer[i];
	}
	return checksum;
}

//function to read from i2c in binary format
//returns usefulsize which is the count of bytes put into the passed buffer
int i2c_frametobufbin(int &fd, unsigned char* const buffer, uint16_t buf_size){
	unsigned char * allbuf;
	uint16_t length_total;
	int usefulcount = 0;
	bool done = false;
	//fill the passed buffer with 0x00s
	memset(buffer, 0x00, buf_size);
	for(int i=0;!done && i<MAX_WAIT;i++){
		unsigned char byte[1];
		uint16_t length = 0;
		if(read(fd, byte, 1) == -1){
	     		printf("unable to read!\n");
	     		return -1;
	  	}
	  	//detect first escape character
	  	if(*byte == I2C_ESCAPE){
	  	//get the next byte to see if we found ourselves a start of frame
	  		if(read(fd, byte, 1)<0){
	  			printf("unable to read!\n");
	     			return -1;	
	  		} else if(*byte == I2C_SOFRAME){
	  			//Start of frame detected, now do the real work
  				//get the length
  				unsigned char buf[2];
  				if(read(fd, buf, 2)< 0){
  					printf("unable to read!\n");
     					return -1;
  				} else {
  					uint16_t l = ((uint16_t)buf[0]<<8) | buf[1];
  					l = le16toh(l); //convert to host order from little endian
  					//std::cout << l << std::endl;
  					length_total = l + 4;
  					//create a buffer big enough for all the data from the frame
  					allbuf = new unsigned char[length_total];
  					allbuf[0] = I2C_ESCAPE;
  					allbuf[1] = I2C_SOFRAME;
  					allbuf[2] = buf[0];
  					allbuf[3] = buf[1];
  					//now get the rest of the frame into this buffer
  					if(l<=buf_size){
  						if(read(fd, &allbuf[4], l+2)<0){
  							printf("unable to read!\n");
     							return -1;
  						} else if (getchecksum(allbuf, length_total) == computechecksum(allbuf, length_total)) {
  							done = true;
  						} else {
  							printf("checksum doesnt match!\n");
  							return -1;
  						}
  					} else {
  						printf("given buffer too small\n");
  						return -1;
  					}
  				}
  			}
  			//if we dont have a start of frame, continue the loop until we find one or rund out of tries
			else continue;
	  	}
	}
	//write the useful stuff to the passed buffer
	for(int i=4,j=0;i<length_total-4;i++,j++){
		buffer[j] = allbuf[i];
		usefulcount++;
	}
	return usefulcount;
}

#endif
