#!/usr/bin/env python
import os
import sys
import errno
from page_loader.arg_parser import create_parser
from page_loader.page_output import download_page
from page_loader.resources_output import download_resources, get_resources
from page_loader.work_with_files import prepare_dir, valid_dir
from page_loader.aux.logs_config import success_logging
from page_loader.aux.custom_exceptions import CommonPageLoaderException


def downloading(url, output_path):
    try:
        output_path = valid_dir(output_path)
        if url == 'no_page':
            #лог, что нет страницы
            sys.exit(1)
        page_path = download_page(url, output_path)
    except (NotADirectoryError, PermissionError, FileNotFoundError, FileExistsError) as e:
        sys.exit(1)
    except CommonPageLoaderException as e:
        sys.exit(1)
    else:
        try:
            new_dir = prepare_dir(url, output_path)
        #success_logging(1, new_dir)
            resources = get_resources(page_path, url, new_dir)
            download_resources(resources, output_path)
            print('success!')
            #можно сделать счетчик, сколько ресурсов загружено, сколько ошибочно
            #success_logging(2, page_path)
        except CommonPageLoaderException as e:
            sys.exit(2)


def main(get_args=create_parser):
    url, output_path = get_args()
    downloading(url, output_path)


if __name__ == '__main__':
    main()
