# web-archiving-scripts

A collection of scripts to help with various web-archiving tasks.

## archived scripts

Contains various scripts for ad-hoc tasks that may or may not be repeated in the future.

## browsertrix-crawler files

Currently contains a custom defaultDriver.js file to automate web crawl behaviours for ICAEW.com

## downloading items from the internet archive

Contains a script to reformat the json response from the Internet Archive's CDX API and provides better duplicate removal. Outputs to a .txt file.

## pdf decrypt

Contains a script to decrypt a folder of PDFs using pikepdf.

## sitemap tools

Contains two scripts. One script produces a plain list of URLs from an XML sitemap (outputs to .txt, .html, or terminal). One script creates a HTML list from a text file input.

## warc_reader.ipynb

A Jupyter notebook that takes a WARC file/collection of WARC files and a list of URLs supplied via .txt file. It then reads the WARC files and determines which URLs are present/missing as specified by the URL list. It also reads and scrapes the HTML content of the URLs specified to search for specific elements in the WARC files.
