#!/bin/bash

echo "SETTING UP AND INSTALLING ENVIRONMENT\n"

sudo apt-get install postgresql
sudo service enable postgresql
sudo service start postgresql
git clone https://github.com/rLoopTeam/eng-software-pi.git
sudo -u postgres createuser -s -d -r rloop
createdb rloopSensor
psql -u rloop -d rloopSensor -f ./eng-software-pi/init/createdb.sql

echo "DB INITIALIZED\n"
