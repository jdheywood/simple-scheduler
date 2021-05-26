import unittest
from unittest.mock import patch

from data_access.models import Job
from data_access.queries import (
    get_all_jobs,
    get_enabled_jobs_by_interval,
    get_job_by_name,
    get_running_jobs,
)

   
@patch('data_access.file.read_jobs_json')
class QueriesTestCase(unittest.TestCase):

    def setUp(self):
        self.test_jobs_dict = {
            "jobs": [
                {
                    "id": 1,
                    "name": "heartbeat",
                    "interval_value": 1,
                    "interval_name": "minutes",
                    "is_running": False,
                    "last_executed": None,
                    "last_outcome": None,
                    "exception": None,
                    "enabled": True
                },
                {
                    "id": 2,
                    "name": "helloworld",
                    "interval_value": 10,
                    "interval_name": "seconds",
                    "is_running": False,
                    "last_executed": None,
                    "last_outcome": None,
                    "exception": None,
                    "enabled": True
                },
                {
                    "id": 3,
                    "name": "testrunningjob",
                    "interval_value": 1,
                    "interval_name": "hours",
                    "is_running": True,
                    "last_executed": None,
                    "last_outcome": None,
                    "exception": None,
                    "enabled": True
                },
            ]
        }

    def test_gets_all_jobs_returns_list_of_job_models(self, read_jobs_json_patch):
        read_jobs_json_patch.return_value = self.test_jobs_dict

        all_jobs = get_all_jobs()

        for job in all_jobs:
            self.assertIsInstance(job, Job)

    def test_get_enabled_jobs_by_interval_returns_list_of_matching_jobs(self, read_jobs_json_patch):
        read_jobs_json_patch.return_value = self.test_jobs_dict

        result = get_enabled_jobs_by_interval(1, 'minutes')

        self.assertIsInstance(result, list)

        for job in result:
            self.assertEqual(job.interval_value, 1)
            self.assertEqual(job.interval_name, 'minutes')

    def test_get_job_by_name_returns_expected_model(self, read_jobs_json_patch):
        read_jobs_json_patch.return_value = self.test_jobs_dict

        expected = Job(
            id=1,
            name='heartbeat',
            interval_value=1,
            interval_name='minutes',
            is_running=False,
            last_executed=None,
            last_outcome=None,
            exception=None,
            enabled=True
        )

        actual = get_job_by_name('heartbeat')

        self.assertEqual(expected, actual)

    def test_get_runing_jobs_returns_jobs_that_are_set_as_running(self, read_jobs_json_patch):
        read_jobs_json_patch.return_value = self.test_jobs_dict

        result = get_running_jobs()
        
        self.assertIsInstance(result, list)

        for job in result:
            self.assertTrue(job.is_running)
