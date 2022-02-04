import numpy as np

def resize(image, plotsize, scale):
    imagetemp = image
    image = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)
    for x in range(int(plotsize/scale)):
        for y in range(int(plotsize/scale)):
            image[x*scale:(x+1)*scale,y*scale:(y+1)*scale] = imagetemp[x,y]
    return image