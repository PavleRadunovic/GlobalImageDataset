
if __name__ == "__main__":
    args, unknown = parser.parse_known_args()
    if args.images_path:
        IMAGES_PATH = args.images_path
    if args.output:
        OUTPUT = args.output   
    images=os.listdir(OUTPUT)
    for i in range(0, 8):
        tiles = os.listdir(OUTPUT + '/' + images[i])
        for j in range(len(tiles)):
            os.rename(OUTPUT + '/' + images[i] + '/' + tiles[j], './sentinel2/trainA/' + images[i] + '_' + tiles[j])
    for i in range(8, len(images)):
        tiles = os.listdir(OUTPUT + '/' + images[i])
        for j in range(len(tiles)):
            os.rename(OUTPUT + '/' + images[i] + '/' + tiles[j], './sentinel2/trainB/' + images[i] + '_' + tiles[j])