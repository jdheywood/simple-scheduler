#!/bin/bash
pidfile="/tmp/looper.pid"

. ~/.bashrc

. venv/bin/activate
cd /home/ubuntu/pipeline-code/code
PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py start

# If using deamonized scheduler uncomment the while, sleep, done and exit lines below
## Loop while the pidfile and the process exist
#while [ -f $pidfile ] && kill -0 $(cat $pidfile) ; do
#    sleep 0.5
#done
#exit 1000 # exit unexpected
