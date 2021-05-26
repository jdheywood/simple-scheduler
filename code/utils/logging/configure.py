import os
import json
import logging.config


def get_logger(default_path='logging-config.json'):
    """
    Setup logging configuration.

    Returns logger for use in your code.
    """
    _configure_logging(default_path)

    return logging.getLogger()


def _configure_logging(default_path='logging-config.json'):
    """
    Setup logging configuration.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = default_path
    full_path = '{}/{}'.format(dir_path, file_path)

    if os.path.exists(full_path):
        with open(full_path, 'rt') as f:
            config = json.load(f)

        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=logging.INFO)
