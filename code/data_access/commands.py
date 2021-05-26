'''
Update data in our data store (poss JSON file on disk for POC)
'''
from data_access.file import read_jobs_json, write_jobs_json


def update_job_is_running_by_job_name(name: str, is_running: bool, filename='jobs.json'):
    jobs_dict = read_jobs_json(filename=filename)

    for job in jobs_dict['jobs']:
        if job['name'] == name:
            job['is_running'] = is_running

    write_jobs_json(jobs_dict, filename=filename)
