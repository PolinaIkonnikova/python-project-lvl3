#!/usr/bin/env python

import sys
from page_loader import create_parser, \
    CommonPageLoaderException, logger, \
    download, user_friendly_message, traceback_message


def main(get_args=create_parser):
    url, output_path = get_args()
    try:
        page_path = download(url, output_path)
        user_friendly_message('success loading', page_path)
        logger.info('The program was completed. Exit Code is 0.')
        sys.exit(0)
    except CommonPageLoaderException:
        logger.warning('The program was completed. Exit Code is 1.')
        sys.exit(1)
    except FileExistsError:
        user_friendly_message('dir exists')
        logger.warning('The program was completed. Exit Code is 2.')
        sys.exit(2)
    except Exception as e:
        logger.warning(f'The unexpected error: {traceback_message(e)}\n'
                       'The program was completed. Exit Code is 1.')
        user_friendly_message('unexpected_err')
        sys.exit(1)


if __name__ == '__main__':
    main()
