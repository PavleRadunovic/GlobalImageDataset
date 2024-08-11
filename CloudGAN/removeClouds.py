import rasterio
import os
import sys
import argparse

IMAGES_PATH = '../tile_operations/outputs'
OUTPUTS = './cloud_removed_images'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default=IMAGES_PATH, type=str,
                    help='The directory with images.')
parser.add_argument('--output', default=OUTPUTS, type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def remove_cloud_from_image(image_path, output_path):
    exec(open("cloudGAN.py").read(), {
     '--img': image_path,
     '--weights_AE': './checkpoints/checkpoint.h5',
     '--config_AE': './checkpoints/config.json',
     '--weights_GAN': './SN-PatchGan-checkpoints',
     '--config_GAN': './cloud_removal/inpaint.yml',
     '--output': output_path,
     '--debug': True
     })

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
    for i in range(len(images)):
        image_tiles = os.listdir(f'{IMAGES_PATH}/{images[i]}')
        if not os.path.exists(f'{OUTPUTS}/{images[i]}'):
            os.makedirs(f'{OUTPUTS}/{images[i]}')
        for j in range(len(image_tiles)):
            print(f'({i+1}/{len(images)}) Remove clouds from image {IMAGES_PATH}/{images[i]}\n')
            print(f"   ({i+j}/{len(image_tiles)}) Tile: {image_tiles[j]}")
            remove_cloud_from_image(f'{IMAGES_PATH}/{images[i]}/{image_tiles(j)}', f'{OUTPUTS}/{images[i]}/{image_tiles(j).replace('.tif','_without_clouds.tif')}')
            if not os.path.exists(f'{OUTPUTS}/{images[i]}/{image_tiles(j).replace('.tif','_without_clouds.tif')}'):
                exit_program()
            set_crs(f'{IMAGES_PATH}/{images[i]}/{image_tiles(j)}', f'{OUTPUTS}/{images[i]}/{image_tiles(j).replace('.tif','_without_clouds.tif')}')
            if os.path.exists(f'{OUTPUTS}/{images[i]}/{image_tiles(j).replace('.tif','_without_clouds.tif')}'):
                os.remove(f'{OUTPUTS}/{images[i]}/{image_tiles(j).replace('.tif','_without_clouds.tif')}')
            break
        print(f'Removing clouds from image {IMAGES_PATH}/{images[i]} done!')
        break
    print('Removing clouds from images done!')
