#!/usr/bin/env python
import argparse
from page_loader.page_output import download


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('--output', type=str, default="home_path",
                        help='your home path')
    parser.add_argument('url', type=str, help='path of loaded file')
    args = parser.parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
