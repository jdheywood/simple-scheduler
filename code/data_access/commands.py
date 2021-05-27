'''
Update data in our data store (poss JSON file on disk for POC)
'''
from datetime import datetime

from data_access.file import read_jobs_json, write_jobs_json


def update_job_is_running_by_job_name(name: str, is_running: bool, filename='jobs.json'):
    jobs_dict = read_jobs_json(filename=filename)

    for job in jobs_dict['jobs']:
        if job['name'] == name:
            job['is_running'] = is_running

    write_jobs_json(jobs_dict, filename=filename)


def update_job_when_started_by_name(name: str, filename='jobs.json'):
    jobs_dict = read_jobs_json(filename=filename)

    for job in jobs_dict['jobs']:
        if job['name'] == name:
            job['is_running'] = True
            job['last_executed'] = datetime.utcnow()

    write_jobs_json(jobs_dict, filename=filename)


def update_job_when_successful_by_name(name: str, filename='jobs.json'):
    jobs_dict = read_jobs_json(filename=filename)

    for job in jobs_dict['jobs']:
        if job['name'] == name:
            job['is_running'] = False
            job['last_outcome'] = 'success'

    write_jobs_json(jobs_dict, filename=filename)


def update_job_when_failed_by_name(name: str, exception: str, filename='jobs.json'):
    jobs_dict = read_jobs_json(filename=filename)

    for job in jobs_dict['jobs']:
        if job['name'] == name:
            job['is_running'] = False
            job['last_outcome'] = 'failed'
            job['exception'] = exception

    write_jobs_json(jobs_dict, filename=filename)


    # TODO change these to be an update_job_from_model function and pass that in, work out the delta, write back to json
