from mpmath import sech
from PIL import Image
import numpy as np

#defined functions
from monoatomicsim import monoasim
from resizer import resize

distulist = []
images = []

initial = 2
final = 1

scale = 8 # resolution of heatmap of electrons

for j in range(2):
    plotsize = 1024
    center = int(plotsize/2)
    size = 0.8
    distuscale = 5*10**2
    distu = [0] * plotsize
    
    for i in range(int(plotsize/2)):
        ii = int(i*2) # Only calculate half of possible area, for performance improvement
        x = (ii-center)/center/(size/3)
        if initial == 2 and final == 1: #If lose an electron
            if j == 0: 
                functionvalue = int(distuscale*(0.4*sech(3.25*x**2) - 0.45*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation
            if j == 1:
                functionvalue = int(distuscale*(sech(2**5*x**2))) # Specific function of particle disturbation
        elif initial == 1 and final == 2: # If gain an electron
            if j == 0: 
                functionvalue = int(distuscale*(sech(2**5*x**2))) # Specific function of particle disturbation
            if j == 1:
                functionvalue = int(distuscale*(0.4*sech(3.25*x**2) - 0.45*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation        
        distu[ii:ii+1] = [functionvalue,functionvalue]
    distulist.append(distu)
    
steps = 5
distusteps = []

for step in range(steps):
    initialshare = np.multiply(distulist[1],(step/(steps-1))) # 100% when first step, 0% when last step
    finalshare = np.multiply(distulist[0],(1-(step/(steps-1))))
    distusteps.append(list(np.add(initialshare, finalshare).astype("int"))) # Find the disturbation line for every stage of motion

graph = []
for i in range(steps):
    graph.append(monoasim(plotsize, center, size, distusteps[i], scale))
    print(f"Processing (1/2) ({i+1}/{len(distusteps)})")
    
for i in range(len(graph)):
    image = (graph[i])[0]
    image2 = (graph[i])[1] # Heatmap
    field = (graph[i])[2] # Electric Field
    
    image = np.multiply(image,128) # color with 128
    
    image2 = resize(image2, plotsize, scale)
    field = resize(field, plotsize, scale)
            
    concat = np.concatenate((image,image2,field), axis=1)
            
    Image.fromarray(np.concatenate((concat,concat,concat), axis=2)).save(f"../images/{i+1}.jpg")
    print(f"Processing (2/2) ({i+1}/{len(distusteps)})")