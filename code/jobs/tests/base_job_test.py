import unittest
from unittest.mock import MagicMock, patch


class BaseJobTest(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.logger = MagicMock()

        get_job_by_name_patch = patch('jobs.base.get_job_by_name')
        self.get_job_by_name = get_job_by_name_patch.start()
        self.addCleanup(get_job_by_name_patch.stop)

        self.model = None

    def set_up_mock_model(self, model_name):
        self.model = MagicMock(is_running=False, last_executed=None, name=model_name)
        self.get_job_by_name.return_value = self.model
