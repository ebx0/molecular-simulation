import numpy as np
from math import dist

def electricfield(data, plotsize, scale):
    plotsize = int(plotsize/8)
    mgplot = np.zeros((plotsize, plotsize, 1), dtype=np.uint8) # Create a new plot to fill, magnitude
    mgdist = [0] * plotsize
    ke = 0.1 # coefficient of electron
    kp = ke*5000 # coefficient of proton
    
    center = int(plotsize/2)
   
    
    for i in range(center): # Take a element in slice
        tempmg = 0 # will be used to store temp magnitude value
        for x in range(len(data)):
            for y in range(len(data)): # And calculate its:
                if data[x,y] > 1:
                    radius = dist([x, y], [i, center]) # Distance to every pixel in data
                    tempmg += ke*(data[x,y] / (1+(radius**2))) # Electric field from electron
        radius = dist([center, center], [i, center])
        tempmg -= (kp / (1+(radius**2)))
        if tempmg > 0:
            mgdist[i] = tempmg
        else:
            mgdist[i] = 255
        
    for x in range(len(mgplot)):
        for y in range(len(mgplot)):
            radius = int(center - dist([x, y], [center, center])+1)
            mgplot[x,y] = (mgdist[radius]) # Electric field
            
    return mgplot
            
    