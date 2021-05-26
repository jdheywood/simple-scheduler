from code.jobs.base import BaseJob


class HelloWorldJob(BaseJob):

    def run(self):
        try:
            self._logger.info('Hello world :-)')

            self.log_success()

        except Exception as ex: # pylint: disable=broad-except
            self._logger.error('Caught an error in job %s', self.model.name, exc_info=True)
            self.log_failure(ex)
