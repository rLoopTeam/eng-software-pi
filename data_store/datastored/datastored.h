#ifndef DATASTORED_H
#define DATASTORED_H

#include <assert.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#include <zmq.h>


#include "rI2CRX.h"

void sighandler(int signum);

void recvParam(struct rI2CRX_decParam decParam);
void gotAFrame();
void endFrame();

#define DAEMONNAME "datalogd"
#define PATH "/mnt/data/log/"
#define PUBLISHER "tcp://127.0.0.1:3000"



#endif
