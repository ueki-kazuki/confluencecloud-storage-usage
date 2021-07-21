# This code sample uses the 'requests' 'json' 'csv' library:
import requests
import json
import csv

#INSERT "USER", "TOKEN", "BASE_URL" HERE
USER="user@example.com"
TOKEN="XXXXXXXXXXXXXXXXX"
BASE_URL="https://example.atlassian.net"

with open('per_page.csv', 'w') as pagecsvfile, open('per_space.csv', 'w') as spacecsvfile:
    perPageWriter = csv.writer(pagecsvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    perSpaceWriter = csv.writer(spacecsvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    perPageWriter.writerow(['pageid','attachment_size(byte)'])
    perSpaceWriter.writerow(['space_name','space_key','attachment_size(byte)'])

    headers = {
       "Accept": "application/json"
    }

    response = requests.request(
       "GET",
       BASE_URL + "/wiki/rest/api/space",
       headers=headers,
       auth=(USER,TOKEN)
    )

    site_attachment_volume = 0 
        
    #Get all space keys
    space_key_results = json.loads(response.text)["results"]
    for space in space_key_results:
        space_attachment_volume = 0 
        #Get related page IDs from space keys
        response = requests.request(
                "GET",
                BASE_URL + "/wiki/rest/api/space/" + space["key"] + "/content",
                headers=headers,
                auth=(USER,TOKEN)
        )   
        print("Space Key: " + space["key"])
        page_results = json.loads(response.text)["page"]["results"]
        for page in page_results:
            page_attachment_volume = 0
            #Get attachments from each page
            print("   " + "Page ID: " + page["id"])
            response = requests.request(
                    "GET",
                    BASE_URL + "/wiki/rest/api/content/" + page["id"] + "/child/attachment",
                    headers=headers,
                    auth=(USER,TOKEN)
            )
            attachment_results = json.loads(response.text)["results"]
            for attachment in attachment_results:
                print("      " + "Attachment Name: " + json.dumps(attachment["title"]) + ", " + json.dumps(attachment["extensions"]["fileSize"]) + " bytes")
                page_attachment_volume += int(json.dumps(attachment["extensions"]["fileSize"]))

            space_attachment_volume += page_attachment_volume
            print("      -->" + "PAGE TOTAL: " + str(page_attachment_volume))

            #Write to CSV
            perPageWriter.writerow([page["id"],str(page_attachment_volume)])

        print("\n         " + "SPACE TOTAL: " + str(space_attachment_volume) + " bytes")
        print("----------")

        #Write to CSV
        perSpaceWriter.writerow([space["name"],space["key"],str(space_attachment_volume)])
