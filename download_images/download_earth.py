from pystac_client import Client
import inquirer
import os
import sys
from datetime import datetime

from input_data import getInputData
from api_requests import make_folder, download_data

OUTPUTS_FOLDER = './outputs'
CLIENT_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION_NAME = "sentinel-2-l2a"

SCRIPT_START = datetime.now()

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

"""
    The main method for downloading satellite images based on date range, cloud coverage, etc.
"""
if __name__ == '__main__':
    make_folder(OUTPUTS_FOLDER)

    [date_range, geometry, query] = getInputData()

    try:
        client = Client.open(CLIENT_URL)
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as error:
        if hasattr(error, 'status_code') and error.status_code == 404:
            print(f"Collection {COLLECTION_NAME} not found!")
        else:
            print(f"Resurs {CLIENT_URL} ne postoji!")
        sys.exit()
    
    if geometry:
        print("\nSearch for data ...\n")
        search = client.search(
            collections=collection,
            intersects=geometry,
            datetime=date_range,
            query=query
        )
        items = list(search.items())
        if len(items) == 0:
            print('There are no images for the selected filters!')
            exit_program()
        itemQuestion = [
            inquirer.Confirm("continue", message=f"There are {len(items)} items. Do you want to continue?", default=True)
        ]
        if inquirer.prompt(itemQuestion)['continue'] == False:
            exit_program()
        
        downloadAllItemsQuestion = [
            inquirer.Confirm("downloadAllItems", message="Do you want to download all of them?", default=True)
        ]
        if inquirer.prompt(downloadAllItemsQuestion)['downloadAllItems']:
            numberOfItems = len(items)
        else:
            numberOfItemsToDownloadQuestion = [
                inquirer.Text("numberOfItemsToDownload", message=f"Enter the number smaller then {len(items)}")
            ]
            numberOfItemsToDownload = int(inquirer.prompt(numberOfItemsToDownloadQuestion)['numberOfItemsToDownload'])
            if numberOfItemsToDownload > len(items) and numberOfItemsToDownload < 1:
                print(f"You can't download more than {len(items)} or less than 1")
                numberOfItemsToDownload = len(items)
            numberOfItems = numberOfItemsToDownload
        
        print("\nDownloading images ...")
        for i in range(numberOfItems):
            TIME_TO_DOWNLOAD_IMAGES = datetime.now()
            itemDict = items[i].to_dict()
            print(f"\n({i+1}/{numberOfItems}) Satellite image {itemDict['id']}:")
            print(f"     - satellite image created at: {datetime.strptime(itemDict['properties']['created'], '%Y-%m-%dT%H:%M:%S.%fZ')}")
            print(f"     - cloud coverage: {itemDict['properties']['eo:cloud_cover']}")

            for key in (itemDict["assets"]):
                if key in ['red', 'green', 'blue']:
                    asset = itemDict["assets"][key]
                    title = asset["title"]
                    href = asset["href"]
                    print(f"           - band name: {title}")
                    if href.startswith("https://"):
                        download_data([[href, 'outputs/' + itemDict['id'] + '/' + key + '.tif']])
            print("Done! --- time to download: " + (datetime.now() - TIME_TO_DOWNLOAD_IMAGES))
        print("Time spent: " + str(datetime.now() - SCRIPT_START))
