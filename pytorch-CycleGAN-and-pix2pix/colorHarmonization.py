import rasterio
import os
import sys
import argparse
import datetime

SCRIPT_START = datetime.datetime.now()

IMAGES_PATH = '../download_images/image_tiles_outputs/'
OUTPUTS = './results'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default=IMAGES_PATH, type=str,
                    help='The directory with images.')
parser.add_argument('--output', default=OUTPUTS, type=str,
                    help='Where to write output.')
parser.add_argument('--model_name', default='sentinel2', type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def colorHarmonization(images_path, output_path, model_name):
    os.system('python ./test.py --dataroot ' + images_path + ' --name ' + model_name + ' --model test --results_dir ' + output_path + ' --num_test 3000 --no_dropout --gpu_ids -1 --preprocess none')

def set_crs(image, tile, source_image_tile, target_image_tile):
    # Open the input image
    with rasterio.open(source_image_tile) as src:
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

        with rasterio.open(target_image_tile) as dest:
            target_image = dest.read()
            with rasterio.open('./pretrained_images/' + image + '/' + tile, "w", **meta) as target_dest:
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
    for i in range(len(images)):
        TIME_START = datetime.datetime.now()
        if not os.path.exists(f'{OUTPUTS}/{images[i]}'):
            os.makedirs(f'{OUTPUTS}/{images[i]}')
        colorHarmonization(f"{IMAGES_PATH}/{images[i]}/RGB", f"{OUTPUTS}/{images[i]}", args.model_name)
        print(f"Color harmonization for image {IMAGES_PATH}/{images[i]} done!, Time spent: {datetime.datetime.now() - TIME_START}")
        image_tiles = len(os.listdir(f'{IMAGES_PATH}/{images[i]}/RGB'))
        print(f'Set coordinate system for image {OUTPUTS}/{images[i]} ...')
        for j in range(len(image_tiles)): 
            print(f"({j+1}/{len(image_tiles)}) ---> {IMAGES_PATH}/{images[i]}/RGB/{image_tiles[j]}")
            set_crs(images[i], image_tiles[j], f"{IMAGES_PATH}/{images[i]}/RGB/{image_tiles[j]}", f"{OUTPUTS}/{images[i]}/{args.model_name}/test_latest/images/{image_tiles[j].replace('.tif', '') + '_real.png'}")

    print(f"Time spent: {datetime.datetime.now() - SCRIPT_START}")
