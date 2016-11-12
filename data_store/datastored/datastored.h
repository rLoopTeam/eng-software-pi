#ifndef DATASTORED_H
#define DATASTORED_H

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <syslog.h>
#include <sys/time.h>
#include <unistd.h>
#include <zmq.h>

#include "createdaemon.h"
#include "zhelpers.h"
#include "rI2CRX.h"

void sighandler(int signum);

void recvParam(struct rI2CRX_decParam decParam);
void gotAFrame();
void endFrame();

#define DAEMONNAME "datalogd"
#define PUBLISHER "tcp://192.168.178.26:3000"



#endif
