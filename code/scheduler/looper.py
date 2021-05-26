import sys
from datetime import timedelta

from timeloop import Timeloop

from data_access.commands import update_job_is_running_by_job_name
from data_access.queries import (
    get_all_jobs,
    get_enabled_jobs_by_interval,
    get_running_jobs,
)
from jobs import (
    HeartbeatJob,
    HelloWorldJob,
)
from utils.logging.configure import get_logger

# from code.process.daemon import Daemon # make Looper inherit from this to fork the process and daemonize the scheduler
from process.angel import Angel # otherwise use a standard process

# Configure and create our logger
logger = get_logger()

# Instantiate our timeloop
tl = Timeloop()

# Define outside class so they are accessible by helper functions
job_classes = {
    'heartbeat': HeartbeatJob,
    'helloworld': HelloWorldJob,
}


def _try_job(model, interval):
    try:
        cls = job_classes[model.name]
    except KeyError:
        raise Exception('No class found for job name')

    if not cls:
        raise Exception('No class found for job name')

    try:
        job = cls(model.name, logger)
    except Exception as e:
        logger.error(e)
        raise

    if not job.is_running():
        logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        logger.info('Starting %s Job %s...\n\n', interval, job.model.name)
        job.log_start()
        job.run()
    else:
        logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        logger.info('%s Job %s already running, skipping this execution\n\n', interval, job.model.name)


class Looper(Angel):
    def __init__(self, pidfile):
        super().__init__(pidfile)

        self._frequencies = [
            '1 seconds',
            '10 seconds',
            '30 seconds',
            '1 minutes',
            '5 minutes',
            '1 hours',
            '1 days',
        ]

    @staticmethod
    @tl.job(interval=timedelta(seconds=1))
    def _every_30_seconds():
        for model in get_enabled_jobs_by_interval(1, 'seconds'):
            _try_job(model, '1secs')

    @staticmethod
    @tl.job(interval=timedelta(seconds=10))
    def _every_30_seconds():
        for model in get_enabled_jobs_by_interval(10, 'seconds'):
            _try_job(model, '10secs')

    @staticmethod
    @tl.job(interval=timedelta(seconds=30))
    def _every_30_seconds():
        for model in get_enabled_jobs_by_interval(30, 'seconds'):
            _try_job(model, '30secs')

    @staticmethod
    @tl.job(interval=timedelta(minutes=1))
    def _every_1_minute():
        for model in get_enabled_jobs_by_interval(1, 'minutes'):
            _try_job(model, '1mins')

    @staticmethod
    @tl.job(interval=timedelta(minutes=5))
    def _every_5_minutes():
        for model in get_enabled_jobs_by_interval(5, 'minutes'):
            _try_job(model, '5mins')

    @staticmethod
    @tl.job(interval=timedelta(hours=1))
    def _every_hour():
        for model in get_enabled_jobs_by_interval(1, 'hours'):
            _try_job(model, '1hrs')

    @staticmethod
    @tl.job(interval=timedelta(days=1))
    def _every_1_day():
        for model in get_enabled_jobs_by_interval(1, 'days'):
            _try_job(model, '1days')

    def run(self):
        logger.info('--------------------------------------')
        logger.info('Looper supports the following frequencies:')
        for frequency in self._frequencies:
            logger.info(frequency)

        logger.info('--------------------------------------')
        all_jobs = get_all_jobs()
        enabled = [job for job in all_jobs if job.enabled]
        disabled = [job for job in all_jobs if not job.enabled]

        logger.info('Looper is aware of the following ENABLED jobs:')
        for job in enabled:
            logger.info('%s, scheduled every: (%s %s)', job.name, job.interval_value, job.interval_name)

        logger.debug('--------------------------------------')
        logger.debug('Looper is aware of the following DISABLED jobs:')
        for job in disabled:
            logger.debug('%s, scheduled every: (%s %s)', job.name, job.interval_value, job.interval_name)

        logger.info('--------------------------------------')
        logger.info('Looking for jobs left in running state')

        for job in get_running_jobs():
            logger.info('Resetting job %s', job.name)
            update_job_is_running_by_job_name(job.name)

        logger.info('--------------------------------------')
        logger.info('Starting up Looper...')

        # Start time loop in main thread using block=True
        # no need to call tl.stop() when start called with block=True
        # https://pypi.org/project/timeloop/
        tl.start(block=True)

    def end(self):
        logger.warning('--------------------------------------')
        logger.warning('Stopping Looper...')
        sys.exit(0)
