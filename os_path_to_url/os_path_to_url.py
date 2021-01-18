#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Takes a directory of files and converts the files in the directory to "pseudo"
URLs or prints the list of files (default).

Built to "rebuild" the URL path of files/directories from a downloaded and
extracted .zip file.
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        description='Takes a directory of files and converts the OS path to a "pseudo URL" or prints the list of files (default).')
    # Requires OS path
    parser.add_argument('os_path', help='OS path')
    # Optional argument to replace root directory with a string
    parser.add_argument(
        '--replace_root', help='argument to replace root directory with a string - i.e. with example.com/')
    # Optional argument to remove file extension
    parser.add_argument('--remove_file_ext',
                        action='store_true', help='removes file extension')
    # Optional argument to write results to file
    parser.add_argument('--to_file', help='name of output .txt file')
    args = parser.parse_args()

    url_list = []
    # Walk path and create a pseudo URL from OS file paths
    for r, d, f in os.walk(args.os_path):
        for file in f:
            # Create entire path
            file = os.path.join(r, file)
            if args.remove_file_ext:
                # Strip the file extension
                file = os.path.splitext(file)[0]
            if args.replace_root:
                # Replace start of os path with HTTP/s location
                file = file.replace(args.os_path, args.replace_root)
            # Replace %20 with -; replace backslash with forward; to lowercase
            file = file.replace(
                '%20', '-').replace("\\", "/").lower()
            url_list.append(file)
            print(file)

    if args.to_file:
        to_file(url_list, args.to_file)


def to_file(urls, filename):
    """Write URL list to file"""
    with open(filename, 'w') as f:
        for i in urls:
            if i == urls[-1]:
                f.write(i)
            else:
                f.write(i+'\n')


if __name__ == '__main__':
    main()
