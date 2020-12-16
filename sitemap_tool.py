#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple tool to produce a plain list of URLs from an XML sitemap. 
Includes basic filtering by 'contains string'.
"""


import argparse
from pathlib import Path
from xml.etree import ElementTree

import requests


def main():
    parser = argparse.ArgumentParser(
        description='A simple tool to produce a plain list of URLs from an XML sitemap.')
    # Requires at least one sitemap URL
    parser.add_argument('sitemap_urls', nargs='+', help='sitemap URL input/s')
    # Optional filtering by 'contains string' argument
    parser.add_argument('--contains_string',
                        help='filter list output by \'contains string\'')
    # Optional save to file
    parser.add_argument('--to_file', help='file path to .txt file output')
    args = parser.parse_args()

    sitemap_urls = get_sitemap_urls(args.sitemap_urls)

    if args.contains_string:
        sitemap_urls = filter_contains_str(sitemap_urls, args.contains_string)

    if args.to_file:
        to_file(sitemap_urls, args.to_file)
    else:
        for i in sitemap_urls:
            print(i)


def get_sitemap_urls(sitemap_urls):
    """Gets sitemap URLs from XML file or website"""
    url_tree = []
    for sitemap in sitemap_urls:
        # Check if XML is local file
        if Path(sitemap).is_file():
            tree = ElementTree.parse(sitemap)
            root = tree.getroot()
            for i in range(len(root)):
                url_tree.append(root[i][0].text)
        # Else read XML from website
        else:
            response = requests.get(sitemap)
            tree = ElementTree.fromstring(response.content)
            for i in range(len(tree)):
                url_tree.append(tree[i][0].text)
    return url_tree


def filter_contains_str(sitemap_urls, contains_string):
    filtered = [i for i in sitemap_urls if contains_string in i]
    return filtered


def to_file(sitemap_urls, filename):
    """Write URL list to file"""
    with open(filename, 'w') as f:
        for i in sitemap_urls:
            if i == sitemap_urls[-1]:
                f.write(i)
            else:
                f.write(i+'\n')


if __name__ == '__main__':
    main()
