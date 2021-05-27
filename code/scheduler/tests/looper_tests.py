from unittest.mock import call, patch, MagicMock

import unittest

from scheduler.looper import Looper


class LooperTestCase(unittest.TestCase): # pylint: disable=too-many-instance-attributes
    def setUp(self):  # sourcery skip: extract-duplicate-method
        logger_patch = patch('scheduler.looper.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

        get_all_jobs_patch = patch('scheduler.looper.get_all_jobs')
        self.get_all_jobs = get_all_jobs_patch.start()
        self.addCleanup(get_all_jobs_patch.stop)

        self.all_jobs = [
            MagicMock(name='job one', interval_value=1, interval_name='days', enabled=True),
            MagicMock(name='job two', interval_value=5, interval_name='hours', enabled=False),
        ]

        get_running_jobs_patch = patch('scheduler.looper.get_running_jobs')
        self.get_running_jobs = get_running_jobs_patch.start()
        self.addCleanup(get_running_jobs_patch.stop)

        self.running_jobs = [
            MagicMock(name='first running job'),
            MagicMock(name='second running job'),
        ]

        update_job_is_running_by_job_name_patch = patch('scheduler.looper.update_job_is_running_by_job_name')
        self.update_job_is_running_by_job_name = update_job_is_running_by_job_name_patch.start()
        self.addCleanup(update_job_is_running_by_job_name_patch.stop)

        timeloop_patch = patch('scheduler.looper.tl')
        self.timeloop = timeloop_patch.start()
        self.addCleanup(timeloop_patch.stop)

    def timeloop_start(self, block=False):
        # assert this is called by run() with a value of True, overriding our default of False
        self.assertTrue(block)

    def test_makes_expected_query_logger_session_and_timeloop_calls_on_run(self):
        self.get_all_jobs.return_value = self.all_jobs
        self.get_running_jobs.return_value = self.running_jobs

        # patch the start function so we don't block execution on main thread during test
        looper = Looper('/tmp/looper.pid')
        with patch.object(self.timeloop, 'start', self.timeloop_start):
            looper.run()

        info_calls = [
            call('--------------------------------------'),
            call('Looper supports the following frequencies:'),
            call('1 seconds'),
            call('10 seconds'),
            call('30 seconds'),
            call('1 minutes'),
            call('5 minutes'),
            call('1 hours'),
            call('1 days'),
            call('--------------------------------------'),
            call('Looper is aware of the following ENABLED jobs:'),
            call('%s, scheduled every: (%s %s)', self.all_jobs[0].name, self.all_jobs[0].interval_value, self.all_jobs[0].interval_name),
            call('--------------------------------------'),
            call('Looking for jobs left in running state'),
            call('Resetting job %s', self.running_jobs[0].name),
            call('Resetting job %s', self.running_jobs[1].name),
            call('--------------------------------------'),
            call('Starting up Looper...')
        ]

        debug_calls = [
            call('--------------------------------------'),
            call('Looper is aware of the following DISABLED jobs:'),
            call('%s, scheduled every: (%s %s)', self.all_jobs[1].name, self.all_jobs[1].interval_value, self.all_jobs[1].interval_name),
        ]

        self.logger.info.assert_has_calls(info_calls)
        self.logger.debug.assert_has_calls(debug_calls)

        self.get_running_jobs.assert_called_once()

        self.update_job_is_running_by_job_name.assert_has_calls([
            call(self.running_jobs[0].name, False),
            call(self.running_jobs[1].name, False),
        ])

    def test_makes_fewer_calls_when_there_are_no_jobs(self):
        self.get_all_jobs.return_value = []
        self.get_running_jobs.return_value = []

        info_calls = [
            call('--------------------------------------'),
            call('Looper supports the following frequencies:'),
            call('1 seconds'),
            call('10 seconds'),
            call('30 seconds'),
            call('1 minutes'),
            call('5 minutes'),
            call('1 hours'),
            call('1 days'),
            call('--------------------------------------'),
            call('Looper is aware of the following ENABLED jobs:'),
            call('--------------------------------------'),
            call('Looking for jobs left in running state'),
            call('--------------------------------------'),
            call('Starting up Looper...')
        ]

        debug_calls = [
            call('--------------------------------------'),
            call('Looper is aware of the following DISABLED jobs:'),
        ]

        # patch the start function so we don't block execution on main thread during test
        looper = Looper('/tmp/looper.pid')
        with patch.object(self.timeloop, 'start', self.timeloop_start):
            looper.run()

        self.logger.info.assert_has_calls(info_calls)
        self.logger.debug.assert_has_calls(debug_calls)

        self.get_running_jobs.assert_called_once()

        self.update_job_is_running_by_job_name.assert_not_called()
