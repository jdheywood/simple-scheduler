'''
Query data from our data store (poss JSON file on disk for POC)
'''
import json
import os

from code.data_access.models import Job


def get_job_by_name(name: str):
    jobs_json = _read_jobs_json()
    for job in jobs_json['jobs']:
        if job['name'] == name:
            return Job(**job)


def get_all_jobs():
    pass


def get_enabled_jobs_by_interval(interval_value: int, interval_name: str):
    pass


def get_running_jobs():
    pass


def _read_jobs_json():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data/jobs.json')) as job_file:
        return json.loads(job_file.read())
