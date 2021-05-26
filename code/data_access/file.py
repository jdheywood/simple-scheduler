import os
import json


def read_jobs_json(filename='jobs.json'):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), f'../../data/{filename}')) as job_file:
        return json.loads(job_file.read())


def write_jobs_json(data, filename='jobs.json'):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), f'../../data/{filename}'), 'w') as job_file:
        json.dump(data, job_file)
