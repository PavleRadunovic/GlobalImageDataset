import rasterio
import numpy as np
import os

def set_crs(source_image_path, source_image_tile):
    # Open the input image
    with rasterio.open('./outputs/' + source_image_path + '/' + source_image_tile) as src:
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

        with rasterio.open('./pretrained_images/' + source_image_path + '/map2sat_pretrained/test_latest/images/' + source_image_tile.replace('.tif', '') + '_real.png') as dest:
            target_image = dest.read()
            with rasterio.open('./results/' + source_image_path + '/' + source_image_tile, "w", **meta) as target_dest:
                target_dest.write(target_image)

if __name__ == "__main__":
    source_images = os.listdir('./outputs')
    for i in range(len(source_images)):
        # Create the output directory if it doesn't exist
        if not os.path.exists('./results/' + source_images[i]):
            os.makedirs('./results/' + source_images[i])
        
        source_image_tiles = os.listdir('./outputs/' + source_images[i])
        for j in range(len(source_image_tiles)):
            set_crs(source_images[i], source_image_tiles[j])
