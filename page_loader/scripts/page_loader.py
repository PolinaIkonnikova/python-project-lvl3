#!/usr/bin/env python

import sys
from page_loader import create_parser
from page_loader import CommonPageLoaderException
from page_loader import download


def main(get_args=create_parser):
    url, output_path = get_args()
    try:
        page_path = download(url, output_path)
        print(f'Cтраница успешно сохранена {page_path}')
        sys.exit(0)
    except CommonPageLoaderException:
        sys.exit(1)
    except FileExistsError:
        sys.exit(2)


if __name__ == '__main__':
    main()
