import numpy as np
from PIL import Image
from mpmath import sech
from math import dist
import random


plotsize = 1024
center = int(plotsize/2)
size = 0.8
distuscale = 5*10**2
distu = [0] * plotsize
scale = 8 #scale of heatmap of particles

    
for i in range(int(plotsize/2)):
   ii = int(i*2) # Only calculate half of possible area, for performance improvement
   x = (ii-center)/center/(size/3)
   functionvalue = int(distuscale*(0.4*sech(3.28*x**2) - 0.45*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation
   distu[ii:ii+1] = [functionvalue,functionvalue]

def monoasim(plotsize, center, size, distu, scale):
    data = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)
    #data2 = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)
    #data3 = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)
    
    distuscale = 5*10**2
    #for i in range(int(len(distu)/2)):
    #    data3[i,0:distu[i]] = [64,16,16]
    
    
    # Lines taken from loop for performance improvement 
    # realdistu = [0] * plotsize
    distu = [i / distuscale for i in distu]
    r0 = int(plotsize/2)
    # Only use loop for areas that an particale can be found
    # realdistuconstant = int(distuscale*8/10**3)
    renderedplot = int(plotsize*size)
    renderedplot2 = int(plotsize*size/3)
    
    # Loop every x and y in rendered plot
    for i in range(renderedplot):
        for j in range(renderedplot):
            x = i+renderedplot2
            y = j+renderedplot2
            radius = int(dist([x, y], [center, center])) # Take the radius of particle
            if random.random()+distu[radius+r0] >= 1: # If its luck+disturbation constant > 1
                data[x,y] = 1 # Paint it
                #realdistu[x] += realdistuconstant # Save the data for analysis
    
    # Draw the real disturbation of particles
    #data2 = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)
    #for i in range(len(realdistu)):
    #    data2[i,-(realdistu[i]+1):-1] = 1
    
    
    # getting an heatmap for particles
    miniplotsize = int(plotsize/scale)
    average = np.zeros((miniplotsize, miniplotsize, 1), dtype=np.uint8)
    for x in range(miniplotsize):
        for y in range(miniplotsize):
            average[x,y] = np.sum(data[x*scale:(x+1)*scale,y*scale:(y+1)*scale])
    average = np.multiply(average, 255/(scale**2)).astype('uint8')
    
    return(data, average)

# Make signals to color
image = np.multiply((monoasim(plotsize, center, size, distu, scale))[0],128)
image2 = (monoasim(plotsize, center, size, distu, scale))[1]

#enlarge the image2 (average map) to normal plot size
imagetemp = image2
image2 = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)
for x in range(int(plotsize/scale)):
    for y in range(int(plotsize/scale)):
        image2[x*scale:(x+1)*scale,y*scale:(y+1)*scale] = imagetemp[x,y]
    

#Image.fromarray(np.concatenate((image,image,image), axis=2)).show()
#Image.fromarray(np.concatenate((image2,image2,image2), axis=2)).show()

