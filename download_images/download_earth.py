from pystac_client import Client
import inquirer
import os
import sys
from datetime import datetime

from input_data import getInputData
from api_requests import make_folder, download_data
from image_proccesing import createTrueColorImage

OUTPUTS_FOLDER = './outputs'
CLIENT_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION_NAME = "sentinel-2-l2a"

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

"""
    The main method ....
    TODO add description
"""
if __name__ == '__main__':
    make_folder(OUTPUTS_FOLDER)

    [date_range, geometry, query, tilename] = getInputData()

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
        # TODO add method for this and add description
        print("\nSearch for data ...\n")
        search = client.search(
            collections=collection,
            intersects=geometry,
            datetime=date_range,
            query=query
        )
        items = list(search.items())
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
            itemDict = items[i].to_dict()
            print(f"\n({i+1}/{numberOfItems}) Satellite image {itemDict['id']}:")
            print(f"     - satellite image created at: {datetime.strptime(itemDict['properties']['created'], '%Y-%m-%dT%H:%M:%S.%fZ')}")
            print(f"     - cloud coverage: {itemDict['properties']['eo:cloud_cover']}")

            for key in (itemDict["assets"]):
                if key in ['red', 'green', 'blue']:
                    asset = itemDict["assets"][key]
                    title = asset["title"]
                    href = asset["href"]
                    print(f"     - band name: {title}")
                    if href.startswith("https://"):
                        download_data([[href, 'outputs/' + itemDict['id'] + '/' + key + '.tif']])
            print("Done!")
                    
    elif tilename:
        # TODO add method for this
        print(tilename)
        pass
