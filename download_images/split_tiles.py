import rasterio
import os
import sys
import argparse
import shutil
import datetime

IMAGES_PATH = './outputs'
OUTPUT = './image_tiles_outputs'
SCRIPT_START = datetime.datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default=IMAGES_PATH, type=str,
                    help='The directory with images.')
parser.add_argument('--output', default=OUTPUT, type=str,
                    help='Where to write output.')

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def split_image(input_file, output_folder, tile_size=256):
    # Open the input image
    with rasterio.open(input_file) as src:
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

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

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
                tile_filename = f"{output_folder}/tile_{i}_{j}.tif"

                # Write the tile to a new file
                with rasterio.open(tile_filename, 'w', driver='GTiff',height=tile_size, width=tile_size, count=src.count, dtype=tile_data.dtype, crs=crs, transform=tile_transform) as dest:
                    dest.write(tile_data)
                    dest.close()

                print(f"Tile {tile_filename} created.")
        src.close()

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        OUTPUT = args.output
    if os.path.exists(IMAGES_PATH):
        images = os.listdir(IMAGES_PATH)
    else:
        exit_program()
    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)
    for i in range(len(images)):
        TIME_TO_CREATE_TILES = datetime.datetime.now()
        print(f"({i+1}/{len(images)}) Create tiles for image {IMAGES_PATH}/{images[i]}")
        split_image(f'{IMAGES_PATH}/' + images[i] + '/red.tif', OUTPUT + '/' + images[i] + '/red')
        split_image(f'{IMAGES_PATH}/' + images[i] + '/green.tif', OUTPUT + '/' + images[i] + '/green')
        split_image(f'{IMAGES_PATH}/' + images[i] + '/blue.tif', OUTPUT + '/' + images[i] + '/blue')    
        red_image_tiles = os.listdir(OUTPUT + '/' + images[i] + '/red')
        if not os.path.exists(OUTPUT + '/' + images[i] + '/trueColor'):
            os.mkdir(OUTPUT + '/' + images[i] + '/trueColor')
        for j in range(len(red_image_tiles)):
            print(f'({j + 1}/{len(red_image_tiles)})')
            os.system(f'gdal_merge.py -separate -o {OUTPUT + '/' + images[i] + '/trueColor/' + red_image_tiles[j]} -co PHOTOMETRIC=RGB {OUTPUT + '/' + images[i] + '/red/' + red_image_tiles[j]} {OUTPUT + '/' + images[i] + '/green/' + red_image_tiles[j]} {OUTPUT + '/' + images[i] + '/blue/' + red_image_tiles[j]}')
        shutil.rmtree(OUTPUT + '/' + images[i] + '/red')
        shutil.rmtree(OUTPUT + '/' + images[i] + '/green')
        shutil.rmtree(OUTPUT + '/' + images[i] + '/blue')
        print("Done! --- time to create tiles: " + (datetime.datetime.now() - TIME_TO_CREATE_TILES))
    print("Time spent: " + str(datetime.datetime.now() - SCRIPT_START))
