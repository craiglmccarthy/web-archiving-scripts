#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rough script to get a report of assets in Preservica.
"""

import csv
import os

from dotenv import load_dotenv
from pyPreservica import *

# Override is needed as the function will load local username instead of from the .env file
load_dotenv(override=True)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
TENANT = os.getenv('TENANT')
SERVER = os.getenv('SERVER')

client = EntityAPI(username=USERNAME,
                   password=PASSWORD, tenant=TENANT, server=SERVER)

# Get root folders
root_folder_references = []
for entity in client.descendants():
    root_folder_references.append(entity.reference)

with open('preservica_assets-trs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Filepath', 'Asset Reference', 'Content Reference',
                    'Filesize (bytes)', 'Date', 'Security tag'])

    # leave argument empty for root folder
    for e in client.all_descendants("9ba88286-6b51-47aa-a265-c782bd2ff286"):

        e = client.entity(e.entity_type, e.reference)
        print(e.title)
        # print(e.reference)
        # print(e.parent)
        # print(folder.reference)
        # print(folder.title)

        if e.parent != None:  # Gets around calling e.parent etc. on root implied root reference in all_descendants()

            filepath_string = []
            folder = client.folder(e.parent)
            filepath_string.insert(0, folder.title + '/')
            while folder.reference not in root_folder_references:  # Get parent folders recursively to the root
                folder = client.folder(folder.parent)
                filepath_string.insert(0, folder.title + '/')

            # comment out to remove folders from output
            if str(e.entity_type) == 'EntityType.FOLDER':
                writer.writerow(
                    [''.join(filepath_string) + e.title, e.reference, '', '', '', e.security_tag])

            if str(e.entity_type) == 'EntityType.ASSET':
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
                                generation.bitstreams[0].length), generation.effective_date, generation.content_object.security_tag])


# for asset in filter(only_assets, client.all_descendants()):
#     e = client.entity(asset.entity_type, asset.reference)

#     for representation in client.representations(asset):
#         print('\nREPRESENTATION:')
#         # print(representation.rep_type)
#         # print(representation.name)
#         print(representation.asset.title)

#         for content_object in client.content_objects(representation):
#             print('\nCONTENT:')
#             print(content_object.reference)
#             print(content_object.title)
#             # print(content_object.description)
#             print(content_object.parent)
#             # print(content_object.metadata)
#             print(content_object.asset.title)

#             for generation in client.generations(content_object):
#                 print('\nGENERATION:')
#                 # print(generation.original)
#                 # print(generation.active)
#                 print(generation.content_object)
#                 print(generation.format_group)
#                 print(generation.effective_date)
#                 print(generation.bitstreams)
#                 print(generation.bitstreams[0].length, 'bytes')

#     # print(e.reference, e.title, e.security_tag,
#     #       f'https://icaew.access.preservica.com/index.php/IO_{e.reference}/')
#     # preservica_assets.writerow([e.reference, e.title, e.security_tag,
#     #                            f'https://icaew.access.preservica.com/index.php/IO_{e.reference}/'])
