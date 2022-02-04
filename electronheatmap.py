import numpy as np

def electronheatmap(data, plotsize, scale):
    miniplotsize = int(plotsize/scale)
    average = np.zeros((miniplotsize, miniplotsize, 1), dtype=np.uint8)
    for x in range(miniplotsize):
        for y in range(miniplotsize):
            average[x,y] = np.sum(data[x*scale:(x+1)*scale,y*scale:(y+1)*scale])
    average = np.multiply(average, 255/(scale**2)).astype('uint8')
    return average