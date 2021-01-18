# web-archiving-tools

A collection of tools to help with web-archiving tasks.

## sitemap_tool.py

```
usage: sitemap_tool.py [-h] [--contains_string CONTAINS_STRING [CONTAINS_STRING ...]] [--to_file TO_FILE] [--to_html TO_HTML] sitemap_input [sitemap_input ...]

A simple tool to produce a plain list of URLs from an XML sitemap. Includes basic filtering by 'contains string'. Outputs to .txt, .html or terminal (default).

positional arguments:
  sitemap_input         sitemap input/s (XML file or URL)

optional arguments:
  -h, --help            show this help message and exit
  --contains_string CONTAINS_STRING [CONTAINS_STRING ...]
                        filter list output by 'contains string', multiple arguments are treated as a Boolean OR search
  --to_file TO_FILE     file path to .txt file output
  --to_html TO_HTML     file path to .html file output
```

## get_html.py

```
usage: get_html.py [-h] [--authenticate] [--file_start FILE_START] [--file_end FILE_END] [--to_json TO_JSON] [--to_pickle TO_PICKLE] url_list

A tool which visits a list of URLs and saves the HTML content to a Python dictionary. Outputs to json, pickle or terminal (default).

positional arguments:
  url_list              .txt file containing list of URLs to visit

optional arguments:
  -h, --help            show this help message and exit
  --authenticate        gives option to provide authentication credentials
  --file_start FILE_START
                        start point of .txt file to read
  --file_end FILE_END   end point of .txt file to read
  --to_json TO_JSON     file path to .json file output
  --to_pickle TO_PICKLE
                        file path to .pkl file output
```

## web-scrape-notebook.ipynb

A Jupyter notebook that takes the pickle file from get_html.py. This notebook can be used to scrape the HTML content contained in the pickle file. Useful for gathering information about a website prior to web-archiving.

## os_path_to_url

Takes a directory of files and converts the OS filepath to a "pseudo URL". Built to "rebuild" the URL path of files/directories from a downloaded and extracted .zip file.

## browser_auto_open.py

```
usage: browser_auto_open.py [-h] (--chrome | --firefox) [--file_start FILE_START] [--file_end FILE_END] [--pywb] [--collection COLLECTION] [--port PORT] url_list

A tool that opens multiple URLs in a browser from a list of URLs supplied via .txt file. Built to be used in conjunction with Python Wayback (PyWb) in record mode.

positional arguments:
  url_list              .txt file containing list of URLs

optional arguments:
  -h, --help            show this help message and exit
  --chrome              mutually exclusive argument, either --chrome or--firefox flags must be provided
  --firefox             mutually exclusive argument, either --chrome or--firefox flags must be provided
  --file_start FILE_START
                        start point of .txt file to read
  --file_end FILE_END   end point of .txt file to read
  --pywb                this flag enables 'pywb record mode' and builds/opens URLs in the form of localhost:{PORT}/{COLLECTION}/record/{URL}
  --collection COLLECTION
                        required flag when 'pywb record mode' is enabled
  --port PORT           required flag when 'pywb record mode' is enabled
```

## xml_metadata_validation.py

A tool to quickly find malformed XML .metadata files. Built to test XML .metadata files prior to ingest into Preservica.
