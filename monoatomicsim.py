import numpy
from PIL import Image
from mpmath import sech
from math import dist
import random


plotsize = 1024
center = int(plotsize/2)
size = 0.8
distuscale = 5*10**2
distu = [0] * plotsize
    
for i in range(int(plotsize/2)):
   ii = int(i*2) # Only calculate half of possible area, for performance improvement
   x = (ii-center)/center/(size/3)
   functionvalue = int(distuscale*(0.4*sech(2*x**2) - 0.4*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation
   distu[ii:ii+1] = [functionvalue,functionvalue]

def monoasim(plotsize, center, size, distu):
    data = numpy.zeros((plotsize, plotsize, 3), dtype=numpy.uint8)
    
    distuscale = 5*10**2
    #for i in range(int(len(distu)/2)):
    #    data[i,0:distu[i]] = [64,16,16]
    
    
    # Lines taken from loop for performance improvement 
    realdistu = [0] * plotsize
    distu = [i / distuscale for i in distu]
    r0 = int(plotsize/2)
    # Only use loop for areas that an particale can be found
    realdistuconstant = int(distuscale*8/10**3)
    renderedplot = int(plotsize*size)
    renderedplot2 = int(plotsize*size/3)
    
    # Loop every x and y in rendered plot
    for i in range(renderedplot):
        for j in range(renderedplot):
            x = i+renderedplot2
            y = j+renderedplot2
            radius = int(dist([x, y], [center, center])) # Take the radius of particle
            if random.random()+distu[radius+r0] >= 1: # If its luck+disturbation constant > 1
                data[x,y] = [64,64,255] # Paint it
                realdistu[x] += realdistuconstant # Save the data for analysis
    
    # Draw the real disturbation of particles
    for i in range(len(realdistu)):
        data[i,-(realdistu[i]+1):-1] = [64,16,16]
    
    image = Image.fromarray(data)
    return(image)

(monoasim(plotsize, center, size, distu)).show()