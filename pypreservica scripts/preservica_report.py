#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rough script to get a report of assets in Preservica.
"""

import csv
import os
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
from pyPreservica import *

# Override is needed as the function will load local username instead of from the .env file
load_dotenv(override=True)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
TENANT = os.getenv('TENANT')
SERVER = os.getenv('SERVER')

CSV_OUTPUT_FILENAME = 'preservica_assets.csv'

client = EntityAPI(username=USERNAME,
                   password=PASSWORD, tenant=TENANT, server=SERVER)

# Get root folders
root_folder_references = []
for entity in client.descendants():
    root_folder_references.append(entity.reference)

with open(CSV_OUTPUT_FILENAME, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Filepath', 'Asset Reference', 'Content Reference',
                    'Filesize (bytes)', 'Date', 'Security tag', 'Title (Metadata)'])

    # Leave argument empty for root folder
    # Filter can be applied via: for asset in filter(only_assets, client.all_descendants()):
    for e in client.all_descendants('83d5a7d0-47a5-46ce-b1f7-21f9a6a2ff0c'):

        print(e)  # Print folder/asset details

        if e.parent != None:  # Gets around calling e.parent etc. on root implied root reference in all_descendants()
            filepath_string = []
            folder = client.folder(e.parent)
            filepath_string.insert(0, folder.title + '/')
            while folder.reference not in root_folder_references:  # Get parent folders recursively to the root
                folder = client.folder(folder.parent)
                filepath_string.insert(0, folder.title + '/')

            # Comment out to remove folders from output
            if str(e.entity_type) == 'EntityType.FOLDER':
                # Get Title from metadata
                folder = client.folder(e.reference)
                for url, schema in folder.metadata.items():
                    # Search the http://www.openarchives.org/OAI/2.0/oai_dc/ schema only
                    if schema == 'http://www.openarchives.org/OAI/2.0/oai_dc/':
                        root = ET.fromstring(client.metadata(url))
                        metadata_title = root[0].text  # Title field
                    else:
                        metadata_title = ''
                writer.writerow(
                    [''.join(filepath_string) + folder.title, folder.reference, '', '', '', folder.security_tag, metadata_title])

            # Comment out to remove assets from output
            if str(e.entity_type) == 'EntityType.ASSET':
                # Get Title from metadata
                asset = client.asset(e.reference)
                for url, schema in asset.metadata.items():
                    # Search the http://www.openarchives.org/OAI/2.0/oai_dc/ schema only
                    if schema == 'http://www.openarchives.org/OAI/2.0/oai_dc/':
                        root = ET.fromstring(client.metadata(url))
                        metadata_title = root[0].text  # Title field
                    else:
                        metadata_title = ''

                for representation in client.representations(e):
                    # print(representation.rep_type)
                    # print(representation.name)
                    # print(representation.asset.title)

                    for content_object in client.content_objects(representation):
                        # print(content_object.reference)
                        # print(content_object.title)
                        # print(content_object.description)
                        # print(content_object.parent)
                        # print(content_object.metadata)
                        # print(content_object.asset.title)

                        for generation in client.generations(content_object):
                            # print('GENERATION:')
                            # print(generation.original)
                            # print(generation.active)
                            # print(generation.content_object)
                            # print(generation.format_group)
                            # print(generation.effective_date)
                            # print(generation.bitstreams)
                            # print(generation.bitstreams[0].length, 'bytes')
                            # print('FILEPATH:', ''.join(filepath_string) + generation.bitstreams[0].filename)
                            # print('SIZE:', generation.bitstreams[0].length)
                            # print('DATE:', generation.effective_date)
                            writer.writerow([''.join(filepath_string) + generation.bitstreams[0].filename, e.reference, generation.content_object.reference, str(
                                generation.bitstreams[0].length), generation.effective_date, generation.content_object.security_tag, metadata_title])
