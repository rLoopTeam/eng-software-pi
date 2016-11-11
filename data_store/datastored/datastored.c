/*
 *
 *
 *
 */

#include "datastored.h"

void sighandler(int signum){
	syslog(LOG_NOTICE, "%s terminated by SIGTERM.", DAEMONNAME);
	exit(EXIT_SUCCESS);
}

int main(int argc, char* argv[]){
	assert( argc = 2);
	char* nodename = argv[1];
	signal(SIGTERM, sighandler);
	//uncomment the next line if you want to compile this as a standalone daemon
	//createdaemon(DAEMONNAME);
	
	syslog(LOG_NOTICE, DAEMONNAME " started.");

	//create a ZMQ-Socket
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
		//create a new file every minute
		time_t time_start = time(NULL);
		char filename[255];
		strftime(filename, sizeof(filename), "/mnt/data/tellog_%Y-%m-%d_%H:%M.csv", gmtime(&time_start));
		FILE *f;
		f = fopen(filename,"a");
		
		//read from socket, write to file
		/*recvCount = zmq_recv(subTelemetry, buffer2, 5000, 0);
		for(int i=0;i<recvCount;i++){
					
		}*/
		char* buffer = s_recv(subTelemetry);
		fprintf(f,"%s,%s\n", nodename, buffer);
		fclose(f);
		free(buffer);
	}	
	
	//We never get here, but ...
	//close ZMQ-Socket
	zmq_close(subTelemetry);
	zmq_ctx_destroy(context);
	
	syslog (LOG_NOTICE, DAEMONNAME " terminated.");
	closelog();

	exit(EXIT_SUCCESS);
}
