import logging
import sys
import os


FORMAT1 = '%(asctime)s - %(levelname)s - %(message)s'
FORMAT2 = '%(message)s'
DATE_FORMAT = '%d-%b-%y %H:%M:%S'


def logs_path():
    work_dir = os.getcwd().split('/')[-1]
    if work_dir == 'tests':
        return '../page_loader/aux/logs.log'
    return 'code/page_loader/aux/logs.log'
    # return 'page_loader/aux/logs.log'


def get_file_handler():
    path = logs_path()
    file_handler = logging.FileHandler(path, 'w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT1,
                                                datefmt=DATE_FORMAT))
    return file_handler


def get_stderr_handler():
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter(FORMAT2))
    return stream_handler


def mistake_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_stderr_handler())
    logger.addHandler(get_file_handler())
    return logger
