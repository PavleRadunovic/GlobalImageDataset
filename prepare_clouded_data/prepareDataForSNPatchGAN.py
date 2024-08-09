import rasterio
import os
import sys
import argparse

IMAGES_PATH = './images'
OUTPUT = './output'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default='./images_for_SN_PatchGAN', type=str,
                    help='The directory with images.')
parser.add_argument('--output', default='./train', type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def split_image(image_path, output_folder, image_name, tile_size=256):
    # Open the input image
    with rasterio.open(image_path) as src:
        # Get image metadata
        meta = src.meta
        width = src.width
        height = src.height

        # Get original transform and CRS
        original_transform = src.transform
        crs = src.crs
        # Update metadata for tiles
        meta.update({
            'height': tile_size,
            'width': tile_size,
            'count': src.count,
            'transform': original_transform,  # This will be updated for each tile
            'crs': crs
        })

        # Iterate through the image and write out tiles
        for i in range(0, width, tile_size):
            for j in range(0, height, tile_size):
                # Define the window for the tile
                window = rasterio.windows.Window(i, j, tile_size, tile_size)
                
                # Read the data for the tile
                tile_data = src.read(window=window)

                 # Compute the transform for the tile
                # Top-left corner of the tile in the original image
                tile_transform = original_transform * rasterio.Affine.translation(i, j)
                

                # Define the output file path
                tile_filename = f"{output_folder}/{image_name}_tile_{i}_{j}.tif"

                # Write the tile to a new file
                with rasterio.open(tile_filename, 'w', driver='GTiff',height=tile_size, width=tile_size, count=src.count, dtype=tile_data.dtype, crs=crs, transform=tile_transform) as dest:
                    dest.write(tile_data)

                print(f"Tile {tile_filename} created.")

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        OUTPUT = args.output
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    if not os.path.exists(IMAGES_PATH) or not os.path.exists(IMAGES_PATH + '/sentinel2/training') or not os.path.exists(IMAGES_PATH + '/sentinel2/validation'):
        exit_program()
    
    training_images = os.listdir(IMAGES_PATH + '/sentinel2/training')
    validation_images = os.listdir(IMAGES_PATH + '/sentinel2/validation')

    print('\nPrepare tiles from training images')
    for i in range(len(training_images)):
        print(f"   ({i+1}/{len(training_images)}) Create tiles for image {IMAGES_PATH}/sentinel2/training/{training_images[i]}")
        if not os.path.exists(f'{IMAGES_PATH}/sentinel2/training/{training_images[i]}'):
            exit_program()
        if not os.path.exists(f'{OUTPUT}/sentinel2/training'):
            os.makedirs(f'{OUTPUT}/sentinel2/training')
        split_image(f'{IMAGES_PATH}/sentinel2/training/{training_images[i]}/true_color.jp2', f'{OUTPUT}/sentinel2/training', training_images[i])
    
    print('\nPrepare tiles from validation images')
    for i in range(len(validation_images)):
        print(f"   ({i+1}/{len(validation_images)}) Create tiles for image {IMAGES_PATH}/sentinel2/validation/{validation_images[i]}")
        if not os.path.exists(f'{IMAGES_PATH}/sentinel2/validation/{validation_images[i]}'):
            exit_program()
        if not os.path.exists(f'{OUTPUT}/sentinel2/validation'):
            os.makedirs(f'{OUTPUT}/sentinel2/validation')
        split_image(f'{IMAGES_PATH}/sentinel2/validation/{validation_images[i]}/true_color.jp2', f'{OUTPUT}/sentinel2/validation', validation_images[i])
        
