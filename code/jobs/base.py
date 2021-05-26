import abc
from datetime import datetime

from utils.exceptions import ScheduledJobException
from data_access.queries import get_job_by_name


class BaseJob(abc.ABC):
    def __init__(self, name, logger):
        self._logger = logger

        self.model = get_job_by_name(name)

        if not self.model:
            raise ScheduledJobException('Error retrieving job model')

    def __del__(self):
        self.model = None

    def is_running(self):
        return self.model.is_running

    def interval(self):
        return '{}_{}'.format(self.model.interval_value, self.model.interval_name)

    def log_start(self):
        self.model.is_running = True
        self.model.last_executed = datetime.utcnow()
 
    @abc.abstractmethod
    def run(self):
        raise NotImplementedError('Jobs must implement the run() method')

    def log_success(self):
        self.model.is_running = False
        self.model.last_outcome = 'success'
        self.model.exception = None

    def log_failure(self, exception):
        self.model.is_running = False
        self.model.last_outcome = 'failed'
        self.model.exception = repr(exception)

        send_notification('Job {} failed, please investigate'.format(self.model.name), 'Scheduled job alert')
