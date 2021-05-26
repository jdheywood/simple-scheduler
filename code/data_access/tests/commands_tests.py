import unittest

from data_access.commands import update_job_is_running_by_job_name
from data_access.file import read_jobs_json


class CommandsTestCase(unittest.TestCase):

    def tearDown(self) -> None:
        update_job_is_running_by_job_name('foo', False, 'test_jobs.json')

    def _get_test_job(self):
        return read_jobs_json(filename='test_jobs.json')['jobs'][0]

    def test_updates_job_is_running_by_name(self):
        # sourcery skip: extract-duplicate-method
        test_job = self._get_test_job()

        self.assertEqual(test_job['name'], 'foo')
        self.assertEqual(test_job['is_running'], False)

        update_job_is_running_by_job_name('foo', True, 'test_jobs.json')

        test_job = self._get_test_job()

        self.assertEqual(test_job['name'], 'foo')
        self.assertEqual(test_job['is_running'], True)
