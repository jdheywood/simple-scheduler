import unittest
from datetime import datetime
from unittest.mock import MagicMock, call, patch

from freezegun import freeze_time
from jobs.heartbeat import HeartbeatJob
from jobs.tests.base_job_test import BaseJobTest


class HeartbeatJobTestCase(BaseJobTest):

    def setUp(self):
        super().setUp()
        self.set_up_mock_model('heartbeat')

    @freeze_time('2019-06-04')
    def test_updates_model_and_persists_state_on_log_start(self):
        heartbeat = HeartbeatJob(self.model.name, self.logger)

        heartbeat.log_start()

        self.assertTrue(self.model.is_running)
        self.assertEqual(self.model.last_executed, datetime(2019, 6, 4))

        # add assertion of data_access function writing to json file (patch that though)

    def test_logs_heartbeat_on_run(self):
        heartbeat = HeartbeatJob(self.model.name, self.logger)

        heartbeat.run()

        self.logger.info.assert_called_with('Heartbeat...')

    def test_updates_model_persists_state_on_log_success(self):
        heartbeat = HeartbeatJob(self.model.name, self.logger)

        heartbeat.log_success()

        self.assertFalse(self.model.is_running)
        self.assertEqual(self.model.last_outcome, 'success')

        # add assertion of data_access function writing to json file (patch that though)

    def test_updates_model_persists_state_on_log_failure(self):
        heartbeat = HeartbeatJob(self.model.name, self.logger)

        exception = {'message': 'Error'}

        heartbeat.log_failure(exception)

        self.assertFalse(self.model.is_running)
        self.assertEqual(self.model.last_outcome, 'failed')

        # add assertion of data_access function writing to json file (patch that though)
