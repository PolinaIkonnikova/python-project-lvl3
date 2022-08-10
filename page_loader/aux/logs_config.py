import logging
import sys


FORMAT1 = '%(asctime)s - %(levelname)s - %(message)s'
FORMAT2 = '%(message)s'
DATE_FORMAT = '%d-%b-%y %H:%M:%S'
# def get_file_handler():
#     path = logs_path()
#     file_handler = logging.FileHandler(path, 'w')
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(logging.Formatter(FORMAT1,
#                                                 datefmt=DATE_FORMAT))
#     return file_handler


def mistake_logger():
    logger = logging.getLogger('warnings')
    stream_err_handler = logging.StreamHandler(stream=sys.stderr)
    stream_err_handler.setLevel(logging.WARNING)
    stream_err_handler.setFormatter(logging.Formatter(FORMAT2))
    stream_err_handler.addFilter(logging.Filter('warnings'))
    logger.addHandler(stream_err_handler)
    return logger


def success_logger():
    logger = logging.getLogger('success')
    logger.setLevel(logging.INFO)
    stream_out_handler = logging.StreamHandler(stream=sys.stdout)
    stream_out_handler.setLevel(logging.INFO)
    stream_out_handler.setFormatter(logging.Formatter(FORMAT1,
                                                      datefmt=DATE_FORMAT))
    logger.addHandler(stream_out_handler)
    return logger


logger1 = success_logger()
logger2 = mistake_logger()


def logging_message(message, error=False):
    if error is False:
        logger1.info(message)
    if error is True:
        logger2.warning(message)
