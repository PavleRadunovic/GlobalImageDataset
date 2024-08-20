import rasterio
import os
import sys
import argparse
import datetime

SCRIPT_START = datetime.datetime.now()

IMAGES_PATH = '../tile_operations/outputs'
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
    os.system('python ./test.py --dataroot ' + images_path + ' --name ' + model_name + ' --model cycle_gan --results_dir ' + output_path + ' --num_test 3000 --no_dropout --gpu_ids -1 --preprocess none')

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
        image_tiles = os.listdir(f'{IMAGES_PATH}/{images[i]}')
        if not os.path.exists(f'{OUTPUTS}/{images[i]}'):
            os.makedirs(f'{OUTPUTS}/{images[i]}')
        colorHarmonization(f"{IMAGES_PATH}/{images[i]}", f"{OUTPUTS}/{images[i]}", args.model_name)
        print(f"Color harmonization for image {IMAGES_PATH}/{images[i]} done!, Time spent: {datetime.datetime.now() - TIME_START}")
    print(f"Time spent: {datetime.datetime.now() - SCRIPT_START}")
