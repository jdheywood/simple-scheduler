'''
Query data from our data store (poss JSON file on disk for POC)
'''
from data_access.file import read_jobs_json
from data_access.models import Job


def get_all_jobs():
    jobs_json = read_jobs_json()
    return [
        Job(**job)
        for job in jobs_json['jobs']
    ]


def get_enabled_jobs_by_interval(interval_value: int, interval_name: str):
    jobs_json = read_jobs_json()
    return [
        Job(**job)
        for job in jobs_json['jobs']
        if job['interval_value'] == interval_value and job['interval_name'] == interval_name
    ]


def get_job_by_name(name: str):
    jobs_json = read_jobs_json()
    for job in jobs_json['jobs']:
        if job['name'] == name:
            return Job(**job)


def get_running_jobs():
    jobs_json = read_jobs_json()
    return [
        Job(**job)
        for job in jobs_json['jobs']
        if job['is_running']
    ]
