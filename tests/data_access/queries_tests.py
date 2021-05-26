import unittest

from code.data_access.models import Job
from code.data_access.queries import get_job_by_name


class GetJobByNameTestCase(unittest.TestCase):

    def test_get_job_by_name_returns_expected_model(self):
        expected = Job(
            1,
            'heartbeat',
            1,
            'minutes',
            False,
            None,
            None,
            None,
            True
        )

        actual = get_job_by_name('heartbeat')

        self.assertEqual(expected, actual)

        print(actual)
