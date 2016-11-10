#ifndef DATASTORED_H
#define DATASTORED_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <syslog.h>
#include <time.h>
#include <zmq.h>

#include "createdaemon.h"
#include "zhelpers.h"

#define DAEMONNAME "datastored"
#define PUBLISHER "tcp://127.0.0.1:3000"

#endif
