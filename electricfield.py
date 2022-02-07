import numpy as np
from math import dist, atan, sin, cos

def electricfield(data, plotsize):
    scale = 8
    plotsize = int(plotsize/scale)
    mgx = np.zeros((plotsize, plotsize, 1), dtype=np.double) # Create a new plot to fill, hortizonal magnitude
    mgy = np.zeros((plotsize, plotsize, 1), dtype=np.double) # Create a new plot to fill, vertical magnitude
    
    mgdist = [0] * plotsize
    ke = 0.05 # coefficient of electron
    kp = ke*2000 # coefficient of proton
    
    center = int((plotsize+1)/2)+1
    
    # Field magnitude
    
    for i in range(center): # Take a element in slice
        tempmg = 0 # will be used to store temp magnitude value
        for x in range(len(data)):
            for y in range(len(data)): # And calculate its:
                if data[x,y] > 1:
                    radius = dist([x, y], [i, center])-1 # Distance to every pixel in data
                    tempmg += ke*(data[x,y] / (1+(radius**2))) # Electric field from electron
        radius = dist([center, center], [i, center])-1
        tempmg -= (kp / (1+(radius**2)))
        if tempmg > 0:
            mgdist[i] = tempmg
        elif tempmg > 255:
            mgdist[i] = 255
            
        
    for x in range(plotsize):
        for y in range(plotsize):
            radius = int((dist([x+1, y+1], [center, center])))
            tempmg = mgdist[int(center-radius)] # Electric field total magnitude
            
    # Find the hortizonal and vertical magnitude with direction of vector
            if x > center:
                try:
                    mgx[x,y] = (cos(atan((center-y)/(center-x)))*tempmg)
                    mgy[x,y] = (sin(atan((center-y)/(center-x)))*tempmg)
                except:
                    mgx[x,y] = (cos(atan((center-y)/(center-x+0.01)))*tempmg)
                    mgy[x,y] = (sin(atan((center-y)/(center-x+0.01)))*tempmg)
            else:
                try:
                    mgx[x,y] = -(cos(atan((center-y)/(center-x)))*tempmg)
                    mgy[x,y] = -(sin(atan((center-y)/(center-x)))*tempmg)
                except:
                    mgx[x,y] = -(cos(atan((center-y)/(center-x+0.01)))*tempmg)
                    mgy[x,y] = -(sin(atan((center-y)/(center-x+0.01)))*tempmg)
            
    return mgx, mgy
            
    