#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A tool to scrape all links on a webpage from a given list of URLs.
Including an option to exclude external links.
"""

import argparse
import getpass
import sys

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

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
    # TODO Optional argument to specify whether to exclude external domain links
    parser.add_argument('--exclude_external',
                        help='exclude external links from final output')
    # TODO Optional save to file
    parser.add_argument('--to_file', help='file path to .txt file output')
    args = parser.parse_args()

    url_list = read_file(args.url_list)

    # Logged in session
    if args.authenticate:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        session_login_page = input('Session login page: ')
        # Add credentials to payload
        payload = {'Username': username,
                   'Password': password, }
        # Return link list from logged in session
        link_list = session(url_list, session_login_page, payload)
    # Regular session
    else:
        # Return link list from regular session
        link_list = scrape_loop(url_list)

    # TODO Optional filters - ADD IF STATEMENT HERE
    link_list = filter_list(link_list)

    # TODO Optional save to file
    if args.to_file:
        to_file(link_list, args.to_file)
    else:
        for i in link_list:
            print(i)

    sys.exit(0)


def filter_list(link_list):
    return link_list


def to_file(sitemap_urls, filename):
    """Write URL list to file"""
    with open(filename, 'w') as f:
        for i in sitemap_urls:
            if i == sitemap_urls[-1]:
                f.write(i)
            else:
                f.write(i+'\n')


def read_file(url_list):
    """Load the .txt file and return list"""
    with open(url_list, 'r') as f:
        lines_file = [line.strip() for line in f]
    return lines_file


def session(url_list, session_login_page, payload):
    """Submit credentials to login"""
    # Set headers / emulate a real browser
    with requests.Session() as sess:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36'}
        res = sess.get(session_login_page, headers=headers)
        # Get validation token by parsing HTML
        signin = BeautifulSoup(res.text, 'html.parser')
        tok = signin.find_all('input')
        # Add token to payload
        payload['__RequestVerificationToken'] = tok[-1]["value"]
        # Submit login details to login page
        res = sess.post(session_login_page, data=payload, headers=headers)

        link_list = scrape_loop(url_list, sess=sess)
        return link_list


def scrape_loop(url_list, sess=False):
    """Main loop for looping through URLs in list"""
    for i in tqdm(url_list):
        if sess == False:
            page = requests.get(i)
        else:
            page = sess.get(i)
        link_list = get_links(page)
    return link_list


def get_links(page):
    """Get links and return list"""
    link_list = []
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.findAll('a')
    try:
        for link in links:
            link_list.append(link["href"])
    except Exception as e:
        print(e)
    return link_list


if __name__ == '__main__':
    main()
