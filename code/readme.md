# Scheduler module

## Overview

```bash
cd code
PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py start
```

This module is responsible for scheduling repeating jobs on our ec2 instance(s).

It makes us of the timeloop package to start jobs on background threads (of the job is not still running since the last execution). To manage this job metadata is serialised to the source database.

The looping code has been wrapped up and turned into a daemon so that it can be run as a background process on our ec2 instance(s) via [supervisord](http://supervisord.org/index.html).

Our configuration of supervisor is delivered via the template file held in our provisioning code here: `ansible/templates/supervisord.conf.j2`.

## Useful commands

Stop the scheduler (so you can tweak the frequency or status of jobs), check running processes via htop after:

```bash
supervisorctl stop scheduler

sudo service supervisor stop

. venv/bin/activate
cd pipeline-code/code
PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py stop

htop
```

Restart and pick up your changes (check htop to see the schedulers processes are running again):

```bash
sudo service supervisor start

htop
```

Tail info.log to watch things happen:

```
tail -f ../logs/info.log
```

Some other handy unix commands when debugging and/or developing a daemon/service are below.

### List all running daemons

`$ ps -eo 'tty,pid,comm' | grep ^?`

### Live tail the log file

`$ tail -f /src/logs/info.log`

### Find process(es) by name

```bash
ps aux | grep -i scheduler
```

### Kill all scheduler processes in one command

```bash
kill $(ps aux | grep 'scheduler/control.py start' | awk '{print $2}')
```

## Notifications

Are set to message dev-notify in Slack when the Schedule job picks up unusual activity, this includes delayed jobs (that are past their last expected execution datetime) and inactive jobs (that have never been executed).

## Running the scheduler locally

To run the scheduler locally you must first ssh into your app container

```bash
docker-compose run --rm app bash
```

Then you need to cd to the code directory and run the python entry point, which is the `control.py` script

```bash
:/src$ cd code

:/src/code$ PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py start
```

Note that valid first arguments to control.py are;

```bash
Usage: scheduler/control.py start|stop|restart
```

## The pidfile

Upon starting up the daemon records it's process identifier, or `pid` in a file (referred to as the class property `pidfile` in the `Daemon` class) on disk in the `/tmp` directory.

The existence of this file indicates that the process is running, and provides a reference to the process id should you wish to track or manipulate this from the operating system.

## Working with Supervisord

There are a few useful commands you may need when working with the scheduler via supervisord on our ec2 instances (staging / production).

### Configuration

The configuration is templated in our `ansible/templates` folder and writes to the file `/etc/supervisor/supervisord.conf` file on our ec2 instances.

If you make changes to this (via changing code locally and pushing/deploying this to the serverd via our CI/CD pipeline) you will need to re-read the configuration file, and also update supervisor to effect these changes, as well as restart supervisor to have these changes take hold.

### Start, stop, restart the scheduler via supervisor

```bash
supervisorctl start|stop|restart scheduler
```

### Re-read the configuration file, but do not restart anything

```bash
supervisorctl reread
```

### Updating applications managed by supervisor that have been reconfigured/changed

```bash
supervisorctl update
```

### Restart supervisor without making config changes available

```bash
sudo service supervisor restart
```

Be warned that this command will not take configuration changes into account, you need to reread and update as described above, restart is useful if you are debugging things on the server or managed apps have crashed and you want supervisor to bring them back up, for example.

### Restart managed application without making config changes available

```bash
supervisorctl restart scheduler
```

You must provide the name as specified in the supervisord.conf file, in our case we only have one, `scheduler`, specified as `[program:scheduler]` in the configuration file.

### Ensure new managed applications are picked up by supervisor

The following commands will stop and start all managed applications, importantly including *new* applications you have added to the configuration file.

```bash
sudo service supervisor stop
sudo service supervisor start
```
