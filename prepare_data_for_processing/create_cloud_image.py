import rasterio
import numpy as np
import os
import sys
import argparse

IMAGES_PATH = './images'
OUTPUT = './outputs'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default='./images', type=str,
                    help='The directory with images.')
parser.add_argument('--output', default='./outputs', type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def calculate_ndvi(b8, b4):
    return (b8 - b4) / (b8 + b4)

def calculate_ndwi(b8, b11):
    return (b8 - b11) / (b8 + b11)

def create_cloud_mask(ndvi, ndwi, ndvi_thresh=0.3, ndwi_thresh=0.3):
    cloud_mask = (ndvi < ndvi_thresh) & (ndwi < ndwi_thresh)
    return cloud_mask

def createCloudedImage(image_path):
    # Open Sentinel-2 bands
    with rasterio.open(image_path + '/B8A.jp2', 'r+') as src:
        src.nodata = 0
        b8 = src.read(1)
    with rasterio.open(image_path + '/B04.jp2', 'r+') as src:
        src.nodata = 0
        b4 = src.read(1)
    with rasterio.open(image_path + '/B11.jp2', 'r+') as src:
        src.nodata = 0
        b11 = src.read(1)

    # Calculate NDVI and NDWI
    ndvi = calculate_ndvi(b8, b4)
    ndwi = calculate_ndwi(b8, b11)

    # Create cloud mask
    cloud_mask = create_cloud_mask(ndvi, ndwi)

    # Save cloud mask
    with rasterio.open(OUTPUT + '/cloud_mask.tif', 'w', **src.meta) as dst:
        dst.write(cloud_mask.astype(rasterio.uint8), 1)

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        MOUTPUT = args.output
    if os.path.exists(IMAGES_PATH):
        images = os.listdir(IMAGES_PATH)
    for i in range(len(images)):
        print(f"({i+1}/{len(images)}) Create cloud mask for image {IMAGES_PATH}/{images[i]}")
        if not os.path.exists(f'{IMAGES_PATH}/' + images[i]):
            exit_program() 
        createCloudedImage(f'{IMAGES_PATH}/' + images[i])