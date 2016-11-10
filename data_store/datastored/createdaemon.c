#include "createdaemon.h"

void createdaemon(char* daemonname) {
	pid_t pid;
	
	//fork off parent process
	pid = fork();
	if(pid < 0) {
		exit(EXIT_FAILURE);	
	}		
	
	//exit parent process
	if(pid > 0){
		exit(EXIT_SUCCESS);	
	}

	//sid for child process, now leader
	if(setsid() < 0) {
		//logging?
		exit(EXIT_FAILURE);	
	}

	//SIGNAL HANDLING goes here

	//fork off a second time
	pid = fork();
	if(pid < 0) {
		exit(EXIT_FAILURE);	
	}		
	
	//exit parent process
	if(pid > 0){
		exit(EXIT_SUCCESS);	
	}
	
	//change filemode mask
	umask(0);

	//change working directory
	if((chdir("/"))<0){
		//logging?
		exit(EXIT_FAILURE);	
	}

	//close standard file descriptors
	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);

	openlog(daemonname, LOG_PID, LOG_DAEMON);
}

