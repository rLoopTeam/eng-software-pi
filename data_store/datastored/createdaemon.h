#ifndef CREATEDAEMON_H
#define CREATEDAEMON_H

#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <syslog.h>
#include <string.h>

void createdaemon(char* daemonname);

#endif
