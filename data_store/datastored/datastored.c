/*
 *
 *
 *
 */

#include "datastored.h"

int main(){
	char* daemonname = "datastored";
	createdaemon(daemonname);
	
	syslog(LOG_NOTICE, "datastored started.");

	//create a ZMQ-Socket
	void *context = zmq_ctx_new();
	void *subTelemetry = zmq_socket(context, ZMQ_SUB);
	int rc = zmq_connect(subTelemetry, PUBLISHER);
	rc = zmq_setsockopt(subTelemetry, ZMQ_SUBSCRIBE, "", strlen(""));
	
	//open the telemetry logfile
	
	while(1){
		sleep(20);
		break;	
	}
	
	//close ZMQ-Socket
	zmq_close(subTelemetry);
	zmq_ctx_destroy(context);
	
	syslog (LOG_NOTICE, "datastored terminated.");
	closelog();

	exit(EXIT_SUCCESS);
}
