import logging
import os


def path_for_log_file():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs.log')


logging.basicConfig(
    level=logging.INFO,
    filename=path_for_log_file(),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filemode='w')


logger = logging.getLogger(__name__)
