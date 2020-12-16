#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A tool to scrape all links on a webpage from a given list of URLs.
Including an option to exclude external links.
"""

import argparse
import getpass

import requests

# TODO 1 Get a list of URLs
# TODO 2 Give option of authenticating
# TODO 3 Loop through list of URLs, visit one page at a time
# TODO 4 Scrape <a> hrefs from page - add to list


def main():
    parser = argparse.ArgumentParser(
        description='A tool to get all links on a webpage from a given list of URLs.')
    # Requires at least one sitemap URL
    parser.add_argument(
        'url_list', help='.txt file containing list of URLs to scrape')
    # Optional argument to give option to provide authentication credentials
    parser.add_argument('--authenticate', action='store_true',
                        help='gives option to provide authentication credentials')
    # Optional argument to specify whether to exclude external domain links
    parser.add_argument('--exclude_external',
                        help='exclude external links from final output')
    # Optional save to file
    parser.add_argument('--to_file', help='file path to .txt file output')
    args = parser.parse_args()

    if args.authenticate:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        session_login_page = input('Session login page: ')

        # TODO Create logged in session; then call function to run rest of program

    x = read_file(args.url_list)

    for i in x:
        print(i)


def read_file(url_list):
    # Load the .txt file and return list
    with open(url_list, 'r') as f:
        lines_file = [line.strip() for line in f]
    return lines_file


if __name__ == '__main__':
    main()
