#ifndef DATASTORED_H
#define DATASTORED_H

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <syslog.h>
#include <time.h>
#include <unistd.h>
#include <zmq.h>

#include "createdaemon.h"
#include "zhelpers.h"

#define DAEMONNAME "datalogd"
#define PUBLISHER "tcp://127.0.0.1:3000"

void sighandler(int signum);

#endif
