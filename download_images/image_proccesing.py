import os
import rasterio

def createTrueColorImage(imagePaths, trueColorPath):
    for path in imagePaths:
        if not os.path.exists(path):
            print(f"File {path} don't exist!")
            return
    if os.path.exists(trueColorPath):
        os.remove(trueColorPath)
    band2=rasterio.open(imagePaths[0]) #blue
    band3=rasterio.open(imagePaths[1]) #green
    band4=rasterio.open(imagePaths[2]) #red
    trueColor = rasterio.open(trueColorPath,'w',driver='Gtiff',
                         width=band4.width, height=band4.height,
                         count=3,
                         crs=band4.crs,
                         transform=band4.transform,
                         dtype=band4.dtypes[0]
                         )
    trueColor.write(band2.read(1),3) #blue
    trueColor.write(band3.read(1),2) #green
    trueColor.write(band4.read(1),1) #red
    trueColor.close()
