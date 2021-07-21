# This code sample uses the 'requests' 'json' 'csv' library:
import csv
import json
import logging
import os
import pprint
import requests
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# INSERT "USER", "TOKEN", "BASE_URL" HERE
USER = os.environ["CONFLUENCE_USER"]
TOKEN = os.environ["CONFLUENCE_TOKEN"]
BASE_URL = os.environ["CONFLUENCE_BASEURL"]

logging.basicConfig(format="%(message)s")
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)


def call(path):
    next_link = path
    while next_link is not None:
        response = requests.request(
            "GET",
            BASE_URL + '/wiki' + next_link,
            headers=headers,
            auth=(USER, TOKEN)
        )
        if not response.ok:
            response.raise_for_status
        try:
            next_link = json.loads(response.text)["_links"]["next"]
        except KeyError:
            next_link = None
        results = json.loads(response.text)["results"]
        for result in results:
            yield result


def get_all_spaces():
    next_link = "/rest/api/space"
    return call(next_link)
    # or
    # yield ({'key': 'ALL', 'name': 'MYSPACE'})
    # yield ({'key': 'DEMO', 'name': 'MY_DEMO_SPACE'})


def get_pages_for(space):
    next_link = "/rest/api/space/" + space["key"] + "/content/page"
    return call(next_link)


def get_attachments_for(page):
    next_link = "/rest/api/content/" + page["id"] + "/child/attachment"
    return call(next_link)


with open('per_page.csv', 'w', encoding='utf-8') as pagecsvfile, open('per_space.csv', 'w', encoding='utf-8') as spacecsvfile:
    perPageWriter = csv.writer(pagecsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    perSpaceWriter = csv.writer(spacecsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    perPageWriter.writerow(['space_name', 'space_key', 'page_title', 'pageid', 'attachment_size(byte)'])
    perSpaceWriter.writerow(['space_name', 'space_key', 'attachment_size(byte)'])

    headers = {
       "Accept": "application/json"
    }

    # Get all space keys
    for space in get_all_spaces():
        logger.debug(pprint.pformat(space))
        space_attachment_volume = 0

        # Get related page IDs from space keys
        logger.info("Space Key: " + space["key"])
        for page in get_pages_for(space):
            logger.debug(pprint.pformat(page))
            page_attachment_volume = 0
            # Get attachments from each page
            logger.info(
                "   Page ID: {:s}  Page Title: {:s}".format(
                    page["id"],
                    page["title"]))

            for attachment in get_attachments_for(page):
                logger.info(
                    "      Attachment Name: {:s}, {:12d} bytes".format(
                        attachment["title"],
                        attachment["extensions"]["fileSize"]))
                page_attachment_volume += attachment["extensions"]["fileSize"]

            space_attachment_volume += page_attachment_volume
            logger.debug(f"      --> PAGE TOTAL: {page_attachment_volume:12d}")

            # Write to CSV
            perPageWriter.writerow([
                space["name"],
                space["key"],
                page["title"],
                page["id"],
                str(page_attachment_volume)])

        logger.info(f"  SPACE TOTAL: {space_attachment_volume:12d} bytes")

        # Write to CSV
        perSpaceWriter.writerow([
            space["name"],
            space["key"],
            str(space_attachment_volume)])
