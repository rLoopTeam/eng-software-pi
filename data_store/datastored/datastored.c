/*
 *	still needs sighandler to handle all!
 *
 *
 */

#include "datastored.h"

// this will point to the .csv
FILE *f;
char filename[255];

void sighandler(int signum){
	syslog(LOG_NOTICE, "%s terminated by SIGTERM.", DAEMONNAME);
	exit(EXIT_SUCCESS);
}

void recvParam(struct rI2CRX_decParam decParam){
	f = fopen(filename,"a");
	fprintf(f,",%d",decParam.index);
	
	switch(decParam.type)

	{

		case rI2C_INT8: fprintf(f,",0x%02x,%d\n",rI2C_INT8,*(int8_t*)(decParam.val));break;

		case rI2C_UINT8: fprintf(f,",0x%02x,%d\n",rI2C_UINT8,*(uint8_t*)(decParam.val));break;

		case rI2C_INT16: fprintf(f,",0x%02x,%d\n",rI2C_INT16,*(int16_t*)(decParam.val));break;

		case rI2C_UINT16: fprintf(f,",0x%02x,%d\n",rI2C_UINT16,*(uint16_t*)(decParam.val));break;

		case rI2C_INT32: fprintf(f,",0x%02x,%d\n",rI2C_INT32,*(int32_t*)(decParam.val));break;

		case rI2C_UINT32: fprintf(f,",0x%02x,%d\n",rI2C_UINT32,*(uint32_t*)(decParam.val));break;

		case rI2C_INT64: fprintf(f,",0x%02x,%ld\n",rI2C_INT64,*(int64_t*)(decParam.val));break;

		case rI2C_UINT64: fprintf(f,",0x%02x,%lu\n",rI2C_UINT64,*(uint64_t*)(decParam.val));break;

		case rI2C_FLOAT: fprintf(f,",0x%02x,%f\n",rI2C_FLOAT,*(float*)(decParam.val));break;

		case rI2C_DOUBLE: fprintf(f,",0x%02x,%f\n",rI2C_DOUBLE,*(double*)(decParam.val));break;

	}
	fclose(f);
}
//writes the gmt-timestamp to the log
void gotAFrame(){
	f = fopen(filename,"a");
	struct timeval 	nowsubsec;
	struct tm now;
	do{
		time_t nowconvert = time(NULL);
		now = *gmtime(&nowconvert);
		gettimeofday(&nowsubsec, NULL);
	}while(nowsubsec.tv_sec != now.tm_sec);
	char timestamp[32];
	strftime(timestamp, sizeof(timestamp), "%T", &now);
	fprintf(f,"%s:%ld",timestamp,nowsubsec.tv_usec);
	fclose(f);
}
void endFrame(){}

int main(int argc, char* argv[]){//int argc, char* argv[]
	assert( argc = 2);
	char* nodename = argv[1];
	signal(SIGTERM, sighandler);
	//uncomment the next line if you want to compile this as a standalone daemon
	//createdaemon(DAEMONNAME);
	
	syslog(LOG_NOTICE, DAEMONNAME " started.");
	
	//
	rI2CRX_begin();
	
	rI2CRX_recvDecParamCB = &recvParam;
	rI2CRX_frameRXBeginCB = &gotAFrame;
	rI2CRX_frameRXEndCB = &endFrame;

	//create a ZMQ-Subscriber
	void *context = zmq_ctx_new();
	void *subTelemetry = zmq_socket(context, ZMQ_SUB);
	int rc = zmq_connect(subTelemetry, PUBLISHER);
	assert( rc ==0);
	rc = zmq_setsockopt(subTelemetry, ZMQ_SUBSCRIBE, "", 0);
	assert( rc ==0);

	uint8_t buffer2[5000];
	int recvCount;
	//main loop
	while(1){
		//read from socket, write to file
		recvCount = zmq_recv(subTelemetry, buffer2, 5000, 0);
		for(int i=0;i<recvCount;i++){
			//create a new file every minute
			time_t time_start = time(NULL);
			strftime(filename, sizeof(filename), "/mnt/data/tellog_%Y-%m-%d_%H:%M.csv", gmtime(&time_start));
			//write the data to file
			rI2CRX_receiveBytes(&buffer2[i],1);		
		}
		//char* buffer = s_recv(subTelemetry);
		//fprintf(f,"%s,%s\n", nodename, buffer);
		
		//free(buffer);
	}	
	
	//We never get here, but ...
	//close ZMQ-Socket
	zmq_close(subTelemetry);
	zmq_ctx_destroy(context);
	
	syslog (LOG_NOTICE, DAEMONNAME " terminated.");
	closelog();

	exit(EXIT_SUCCESS);
}
