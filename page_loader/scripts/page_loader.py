#!/usr/bin/env python

import sys
from page_loader import create_parser, \
    CommonPageLoaderException, logger, \
    download, user_friendly_message, \
    traceback_message, path_for_log_file


def read_logs(logs):
    if logs:
        with open(path_for_log_file(), 'r') as f:
            print(f.read())


def main(get_args=create_parser):

    url, output_path, logs = get_args()

    try:
        page_path = download(url, output_path)
        user_friendly_message('success loading', page_path)
        logger.info('The program was completed. Exit Code is 0.')
        read_logs(logs)
        sys.exit(0)
    except CommonPageLoaderException:
        logger.warning('The program was completed. Exit Code is 1.')
        read_logs(logs)
        sys.exit(1)
    except FileExistsError:
        user_friendly_message('dir exists')
        logger.warning('The program was completed. Exit Code is 2.')
        read_logs(logs)
        sys.exit(2)
    except Exception as e:
        logger.warning(f'The unexpected error: {traceback_message(e)}\n'
                       'The program was completed. Exit Code is 1.')
        user_friendly_message('unexpected_err')
        read_logs(logs)
        sys.exit(1)


if __name__ == '__main__':
    main()
