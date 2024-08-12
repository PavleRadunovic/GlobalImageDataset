import rasterio
import os
import sys
import argparse
import datetime

now = datetime.datetime.now()

IMAGES_PATH = '../tile_operations/outputs'
OUTPUTS = './results'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default=IMAGES_PATH, type=str,
                    help='The directory with images.')
parser.add_argument('--output', default=OUTPUTS, type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def colorHarmonization(images_path, output_path):
    os.system(f"python ./test.py --dataroot {images_path} --name map2sat_pretrained --model test --results_dir {output_path} --num_test 3000 --no_dropout")

def set_crs(source_image_path, target_image_path):
    # Open the input image
    with rasterio.open(source_image_path) as src:
        # Get image metadata
        meta = src.meta
        width = src.width
        height = src.height

        # Get original transform and CRS
        original_transform = src.transform
        crs = src.crs

        # Update metadata for tiles
        meta.update({
            'height': height,
            'width': width,
            'count': src.count,
            'transform': original_transform,
            'crs': crs
        })

        with rasterio.open(target_image_path) as dest:
            target_image = dest.read()
            with rasterio.open(target_image_path.replace('_without_clouds', ''), "w", **meta) as target_dest:
                target_dest.write(target_image)

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        OUTPUTS = args.output
        if not os.path.exists(OUTPUTS):
            os.makedirs(OUTPUTS)
    images = os.listdir(IMAGES_PATH)
    #for i in range(len(images)):
    for i in range(0, 1):
        image_tiles = os.listdir(f'{IMAGES_PATH}/{images[i]}')
        if not os.path.exists(f'{OUTPUTS}/{images[i]}'):
            os.makedirs(f'{OUTPUTS}/{images[i]}')
        colorHarmonization(f"{IMAGES_PATH}/{images[i]}", f"{OUTPUTS}/{images[i]}")
        print(f"Color harmonization for image {IMAGES_PATH}/{images[i]} done!")
    print(datetime.datetime.now() - now)
