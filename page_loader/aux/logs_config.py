import logging
import sys


MISTAKE_MESSAGES = {1: "The main error: {}",
                    2: "Seems '{}' is not a html page! Try again.",
                    3: "This directory '{}' doesn't exist. Please change another directory!",
                    4: "You doesn't have access rights for '{}', please choose another directory!",
                    5: "The directory '{}' already exists",
                    6: {
                        '5XX': "The server failed to fulfil a request for {}. Status code is {}.",
                        '4XX': "Response is 4XX, {}, {}",
                        '3XX': "Response is 3XX, {}, {}",
                        '404': "The requested resource {} could not be found. Status code is {}."
                    },
                    7: 'Problems with connecting for {}. Status code is {}'}

SUCCESS_MESSAGES = { 1: "The resource directory was created - {}.",
                     2: "The page was loaded as {}.",
                     3: "Нет ресурсов для скачивания."}


FORMAT1 = '%(asctime)s - %(levelname)s - %(message)s'
FORMAT2 = '%(message)s'


def get_stdout_handler():
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(FORMAT2))
    return stream_handler


def get_file_handler():
    file_handler = logging.FileHandler("page_loader/aux/logs.log", 'wb')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT1, datefmt='%d-%b-%y %H:%M:%S'))
    return file_handler


def get_stderr_handler():
    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(logging.Formatter(FORMAT2))
    return stream_handler


def messanger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_stdout_handler())
    logger.addHandler(get_file_handler())
    return logger


def mistake_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_stderr_handler())
    logger.addHandler(get_file_handler())
    return logger


def mistakes_logging(exc, case, *args, exit=True):
    logger = mistake_logger(__name__)
    logger.warning(MISTAKE_MESSAGES[1].format(exc))
    if exit is True:
        logger.error(MISTAKE_MESSAGES[case].format(*args))
    elif exit is False:
        logger.debug(MISTAKE_MESSAGES[case].format(*args))
    #logger.error(MISTAKE_MESSAGES[case].format(*args))


# def requests_logging(exc, code, url, exit=False):
#     agr = '404'
#     num = str(code)[0]
#     logger = mistake_logger(__name__)
#     if num == 4:
#         agr = '4XX' # сделать вариативность кодов
#     elif num == 5:
#         agr = '5XX'
# #    elif num == 404:
# #       agr = '4XX'
#     elif num == 3:
#         agr = '3XX'
#     logger.debug(MISTAKE_MESSAGES[1].format(exc))

   # if exit is True:
   #     logger.error(MISTAKE_MESSAGES[6][agr].format(url, code))
   # elif exit is False:
   #     logger.debug(MISTAKE_MESSAGES[6][agr].format(url, code))


def success_logging(case, *args):
    logger = messanger(__name__)
    logger.info(SUCCESS_MESSAGES[case].format(*args))
