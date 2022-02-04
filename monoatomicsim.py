import numpy as np
from PIL import Image
from mpmath import sech
from math import dist
import random

# Defined functions
from electronheatmap import electronheatmap
from electricfield import electricfield
from resizer import resize



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
    
    distuscale = 5*10**2
    
    distu = [i / distuscale for i in distu]
    r0 = int(plotsize/2)
    # Only use loop for areas that an particale can be found
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

    
    # Getting an heatmap for particles
    average = electronheatmap(data, plotsize, scale)
    
    # Calculate the electric field of plot
    field = electricfield(average, plotsize, scale)
    
    return(data, average, field)

# Make signals to color
image = np.multiply((monoasim(plotsize, center, size, distu, scale))[0],128)
image2 = (monoasim(plotsize, center, size, distu, scale))[1]
field = (monoasim(plotsize, center, size, distu, scale))[2]

#enlarge the scaled plots to normal plot size
image2 = resize(image2, plotsize, scale)
field = resize(field, plotsize, scale)

    

#Image.fromarray(np.concatenate((image,image,image), axis=2)).show()
#Image.fromarray(np.concatenate((image2,image2,image2), axis=2)).show()
#Image.fromarray(np.concatenate((field,field,field), axis=2)).show()


