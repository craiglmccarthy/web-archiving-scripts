#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A tool to scrape all links on a webpage from a given list of URLs from .txt file.
"""

import argparse
import getpass
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(
        description='A tool to get all links on a webpage from a given list of URLs.')
    # Requires at least one sitemap URL
    parser.add_argument(
        'url_list', help='.txt file containing list of URLs to scrape')
    # Optional argument to give option to provide authentication credentials
    parser.add_argument('--authenticate', action='store_true',
                        help='gives option to provide authentication credentials')
    # Optional argument to give start point of URLs to visit
    parser.add_argument('--file_start', type=int,
                        help='start point of URLs to visit')
    # Optional argument to give end point of URLs to visit
    parser.add_argument('--file_end', type=int,
                        help='end point of URLs to visit')
    # TODO Optional save to file
    parser.add_argument('--to_file', help='file path to .txt file output')
    args = parser.parse_args()

    # Read file into list
    url_list = read_file(args.url_list)

    # Where to read from and to; default is entire list
    if args.file_start:
        start = args.file_start
    else:
        start = 0
    if args.file_end:
        end = args.file_end
    else:
        end = len(url_list)
    # Change list depending on given start:end parameters
    url_list = url_list[start:end]

    # Logged in session
    if args.authenticate:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        session_login_page = input('Session login page: ')
        # Add credentials to payload
        payload = {'Username': username,
                   'Password': password, }
        # Return link list from logged in session
        dict_page_links = session(url_list, session_login_page, payload)
    # Regular session
    else:
        # Return link list from regular session
        dict_page_links = scrape_loop(url_list)

    # Print dictionary
    # for item in dict_page_links.items():
    #     print(item)
    #     print('\n\n')

    df = pd.DataFrame.from_dict(dict_page_links, orient='index')
    df.to_excel("output.xlsx")

    sys.exit(0)


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

        dict_page_links = scrape_loop(url_list, sess=sess)
        return dict_page_links


def scrape_loop(url_list, sess=False):
    """Main loop for looping through URLs in list. Building dictionary of
    pages (key) and links (values)"""
    dict_page_links = {}
    for i in tqdm(url_list):
        try:
            if sess == False:
                page = requests.get(i)
            else:
                page = sess.get(i)
        except Exception as e:
            print(e)
        link_list = get_links(page)
        # Update dictionary with new key:value pairs
        dict_page_links.update({i: link_list})
    return dict_page_links


def get_links(page):
    """Get links and return list"""
    link_list = []
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.findAll('a')
    for link in links:
        try:
            link_list.append(link["href"])
        except Exception as e:
            print(e)
    return link_list


if __name__ == '__main__':
    main()
