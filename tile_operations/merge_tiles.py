import numpy as np
import rasterio
from rasterio.merge import merge
import os

# If we receive an error: rasterio.errors.RasterioIOError: ... Too many open files
# Try this: ulimit -n 50000

def merge_tiles(tile_paths, source_image):
    # Open all tiles and prepare them for merging
    src_files_to_mosaic = []
    for tile_path in tile_paths:
        if tile_path.endswith('.tif'):
            src = rasterio.open('./results/' + source_image + '/' + tile_path)
            src_files_to_mosaic.append(src)

    # Merge tiles into a single image
    mosaic, out_trans = merge(src_files_to_mosaic)

    # Write the mosaic to the output file
    with rasterio.open(
        './color_harmonized_images/' + source_image + '.tif', 'w', driver='GTiff',
        height=mosaic.shape[1], width=mosaic.shape[2],
        count=len(src_files_to_mosaic[0].read()),  # assuming all tiles have same number of bands
        dtype=mosaic.dtype,
        crs=src_files_to_mosaic[0].crs,
        transform=out_trans
    ) as dst:
        dst.write(mosaic)

    # Close all sources
    for src in src_files_to_mosaic:
        src.close()

if __name__ == "__main__":
    source_images = os.listdir('./results')
    for i in range(len(source_images)):
        source_image_tiles = os.listdir('./results/' + source_images[i])
        merge_tiles(source_image_tiles, source_images[i])