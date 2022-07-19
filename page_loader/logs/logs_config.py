import logging
import os
import sys


def make_logger():
    #log_path = os.path.join(os.getcwd(), 'page_loader/logs/logs.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        #handlers=[logging.FileHandler(log_path, 'w')]
                        stream=sys.stderr
                        )
    logger = logging.getLogger(__name__)
    return logger


def make_loggers():
    log_path = os.path.join(os.getcwd(), 'page_loader/logs/logs.log')
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(log_path, 'w')],
                        datefmt='%d-%b-%y %H:%M:%S')

    text_logger = logging.getLogger(__name__)
    text_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_path, 'w')
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
    text_logger.addHandler(handler)

    stderr_logger = logging.getLogger(__name__)
    stderr_logger.setLevel(logging.DEBUG)
    handler2 = logging.StreamHandler(stream=sys.stderr)
    stderr_logger.addHandler(handler2)
    return stderr_logger, text_logger

