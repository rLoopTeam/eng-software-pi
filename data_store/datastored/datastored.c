/*
 *
 *
 *
 */

#include "datastored.h"

int main(){
	createdaemon(DAEMONNAME);
	
	syslog(LOG_NOTICE, DAEMONNAME " started.");

	//create a ZMQ-Socket
	void *context = zmq_ctx_new();
	void *subTelemetry = zmq_socket(context, ZMQ_SUB);
	int rc = zmq_connect(subTelemetry, PUBLISHER);
	assert( rc ==0);
	rc = zmq_setsockopt(subTelemetry, ZMQ_SUBSCRIBE, "", 0);
	assert( rc ==0);

	//main loop
	while(1){
		//create a new file every minute
		time_t time_start = time(NULL);
		char filename[255];
		strftime(filename, sizeof(filename), "/mnt/data/tellog_%Y-%m-%d_%H:%M.txt", gmtime(&time_start));
		FILE *f;
		f = fopen(filename,"a");
		
		//read from socket, write to file
		char* buffer = s_recv(subTelemetry);
		fprintf(f,"%s\n",buffer);
		fclose(f);
		free(buffer);
	}	
	
	//close ZMQ-Socket
	zmq_close(subTelemetry);
	zmq_ctx_destroy(context);
	
	syslog (LOG_NOTICE, DAEMONNAME " terminated.");
	closelog();

	exit(EXIT_SUCCESS);
}
