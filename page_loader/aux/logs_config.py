import logging
import sys
import os


# MISTAKE_MESSAGES = {1: "The main error: {}",
#                     2: "Seems '{}' is not a html page! Try again.",
#                     3: "This directory '{}' doesn't exist. Please change another directory!",
#                     4: "You doesn't have access rights for '{}', please choose another directory!",
#                     5: "The directory '{}' already exists",
#                     6: {
#                         '5XX': "The server failed to fulfil a request for {}. Status code is {}.",
#                         '4XX': "Response is 4XX, {}, {}",
#                         '3XX': "Response is 3XX, {}, {}",
#                         '404': "The requested resource {} could not be found. Status code is {}."
#                     },
#                     7: 'Problems with connecting for {}. Status code is {}'}
#
# SUCCESS_MESSAGES = { 1: "The resource directory was created - {}.",
#                      2: "The page was loaded as {}.",
#                      3: "Нет ресурсов для скачивания."}

log_path = os.path.join(os.getcwd(), 'page_loader/aux/logs.log')
FORMAT1 = '%(asctime)s - %(levelname)s - %(message)s'
FORMAT2 = '%(message)s'


def get_file_handler():
    file_handler = logging.FileHandler(log_path, 'w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT1, datefmt='%d-%b-%y %H:%M:%S'))
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
