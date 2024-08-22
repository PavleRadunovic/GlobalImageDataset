import numpy as np
import rasterio
from rasterio.merge import merge
import os
import sys
import argparse

# If we receive an error: rasterio.errors.RasterioIOError: ... Too many open files
# Try this: ulimit -n 50000

IMAGES_PATH = '../pytorch-CycleGAN-and-pix2pix/pretrained_images'
MOSAIC_OUTPUT = './images'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default=IMAGES_PATH, type=str,
                    help='The directory with images.')
parser.add_argument('--output', default=MOSAIC_OUTPUT, type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def create_mosaic(images_path, mosaic_name):
    # Open all images and prepare them for merging
    src_files_to_mosaic = []
    for image_path in images_path:
        if image_path.endswith('.tif'):
            src = rasterio.open(IMAGES_PATH + '/' + image_path)
            src_files_to_mosaic.append(src)

    # Merge images into a single image
    mosaic, out_trans = merge(src_files_to_mosaic)

    # Write the mosaic to the output file
    with rasterio.open(
        MOSAIC_OUTPUT + '/' + mosaic_name, 'w', driver='GTiff',
        height=mosaic.shape[1], width=mosaic.shape[2],
        count=len(src_files_to_mosaic[0].read()),  # assuming all tiles have same number of bands
        dtype=mosaic.dtype,
        crs=src_files_to_mosaic[0].crs,
        transform=out_trans
    ) as dst:
        dst.write(mosaic)
        dst.close()

    # Close all sources
    for src in src_files_to_mosaic:
        src.close()

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        MOSAIC_OUTPUT = args.output
    images_path = os.listdir(IMAGES_PATH)
    for i in range(len(images_path)):
        if os.path.exists(IMAGES_PATH + '/' + images_path[i]):
            source_images_path = os.listdir(IMAGES_PATH + '/' + images_path[i])
            create_mosaic(source_images_path, images_path[i])
        else:
            exit_program()