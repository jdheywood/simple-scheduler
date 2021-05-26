# pylint: disable=unnecessary-pass
"""
Contains custom exceptions
"""


class ScheduledJobException(Exception):
    """
    Raised when an issue is found during execution of tasks defined as scheduled jobs
    """
    pass
