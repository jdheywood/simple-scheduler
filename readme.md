# Simple Scheduler

Do you need to run some code on a regular basis?

Do you want something lightweight and fairly simple to do this?

Do you just want some python code, without the bloat of a big old framework or platform?

Then look no further friend, welcome to your new simple scheduler, written in pure python, no filler all thriller.

## Setup

### Create a virtualenv

```bash
$ pip3 install virtualenv
...
$ virtualenv -p python3 ./venv
...
$ . venv/bin/activate
...
$ python
Python 3.9.4 (default, Apr  5 2021, 01:50:46) 
>>> 
>>> exit()
```

### Install requirements

```bash
$ pip install -r requirements.txt
...
Successfully installed ...
```

### Run the tests

```bash
$ nosetests -w code --verbose --nocapture --rednose
```

## Run the scheduler

```bash
cd code
PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py start
```

This code allows the scheduling of repeating jobs on pre-defined frequencies.

It makes us of the [timeloop](https://pypi.org/project/timeloop/) package to start jobs on a recurring interval (if the jobs are not still running since the last execution). To manage this, job metadata is serialised to a json file.

The jobs can be set to run on a background thread, if the `Looper` class inherits from the `Daemon` process class. To run the jobs in the main thread `Looper` should inherit from the `Angel` process class.

For deploying to a remote environment (such as production for example) it would be wise to manage the scheduler via some form of process manager such as [supervisor](http://supervisord.org/index.html) for example.

## Further control of Daemonised Looper

When running as a daemon process you can stop and restart the running scheduler via teh following commands:

```bash
PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py stop

PYTHONPATH=$PYTHONPATH:$(pwd) python scheduler/control.py restart
```
Note that valid first arguments to control.py are;

```bash
Usage: scheduler/control.py start|stop|restart
```

As stdout is no longer available when running in the background you can watch the output of the scheduler via the logs, for example you can tail info.log to watch things happen:

```
tail -f ../logs/info.log
```

## Handy unix commands when debugging and/or developing a daemon/service

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

## The pidfile

Upon starting up the daemon records it's process identifier, or `pid` in a file (referred to as the class property `pidfile` in the `Daemon` class) on disk in the `/tmp` directory.

The existence of this file indicates that the process is running, and provides a reference to the process id should you wish to track or manipulate this from the operating system.
