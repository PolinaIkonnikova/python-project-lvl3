import os
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url', type=str, default="no_page",
                        help='url for downloading')
    parser.add_argument('-o', '--output', type=str, default=os.getcwd(),
                        help='A path for new page '
                             '(default: your current directory)')
    args = parser.parse_args()
    return args.url, args.output
