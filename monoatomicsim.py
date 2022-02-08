import numpy as np
from math import dist
import random


# Defined functions
from electronheatmap import electronheatmap
from electricfield import electricfield
from resizer import resize
from distugraph import distugraph


plotsize = 512

distu = distugraph(1, plotsize) # Get the disturbation graph of elements 

# define the function of simulate one atoms image and data
def monoasim(plotsize, distu):
    center = int(plotsize/2)
    data = np.zeros((plotsize, plotsize, 1), dtype=np.uint8)

    r0 = int(plotsize/2)
    
    # Loop every x and y in rendered plot
    for x in range(plotsize):
        for y in range(plotsize):
            radius = int(dist([x, y], [center, center])) # Take the radius of particle
            if radius+r0 <= plotsize:
                if random.random()+distu[radius+r0] >= 1: # If its luck+disturbation constant > 1
                    data[x,y] = 1 # Paint it
    
    # Getting an heatmap for particles
    average = electronheatmap(data, plotsize)
    # Calculate the electric field of plot
    field = electricfield(average, plotsize)
    
    return(data, average, field)


# Make signals to color
returnvalue = (monoasim(plotsize, distu))

image = np.multiply(returnvalue[0],128) # exact locations of electrons
image2 = (returnvalue)[1] # average electron map

fieldx = (returnvalue)[2][0] # hortizonal electric field, 127 = zero field
fieldy = (returnvalue)[2][1] # vertical of electric field, 127 = zero field

# Enlarge the scaled plots to normal plot size
image2 = resize(image2, plotsize)
fieldx = resize(fieldx, plotsize)
fieldy = resize(fieldy, plotsize)

# Show them
#from PIL import Image
#Image.fromarray(np.concatenate((image,image,image), axis=2)).show()
#Image.fromarray(np.concatenate((image2,image2,image2), axis=2)).show()
#Image.fromarray(np.concatenate((fieldx,fieldx,fieldx), axis=2)).show()


