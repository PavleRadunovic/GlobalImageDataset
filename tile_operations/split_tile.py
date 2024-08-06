import rasterio
import os
import sys
import argparse

IMAGES_PATH = '../download_images/outputs'
OUTPUT = './output'

parser = argparse.ArgumentParser()
parser.add_argument('--images_path', default='./images', type=str,
                    help='The directory with images.')
parser.add_argument('--output', default='./outputs', type=str,
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

                print(f"Tile {tile_filename} created.")

if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        MOUTPUT = args.output
    if os.path.exists(IMAGES_PATH):
        images = os.listdir(IMAGES_PATH)
    for i in range(len(images)):
        print(f"({i+1}/{len(images)}) Create tiles for image {IMAGES_PATH}/{images[i]}/trueColor.tif")
        if not os.path.exists(f'{IMAGES_PATH}/' + images[i] + '/trueColor.tif'):
            exit_program() 
        split_image(f'{IMAGES_PATH}/' + images[i] + '/trueColor.tif', OUTPUT + '/' + images[i])
