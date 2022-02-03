from mpmath import sech
from PIL import Image
from monoatomicsim import monoasim
import numpy as np

distulist = []
images = []

initial = 2
final = 1

scale = 8 # resolution of heatmap of electrons

#Will be rewrite. Currently unavalible
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
    
steps = 120
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

    image = np.multiply(image,128) # color with 128
    
    imagetemp = image2 # to upscale the heatmap
    image2 = np.zeros((plotsize, plotsize, 1), dtype=np.uint8) # upscaled blank plot to paint
    for x in range(int(plotsize/scale)):
        for y in range(int(plotsize/scale)):
            image2[x*scale:(x+1)*scale, y*scale:(y+1)*scale] = imagetemp[x,y]
            
    concat = np.concatenate((image,image2), axis=1)
            
    Image.fromarray(np.concatenate((concat,concat,concat), axis=2)).save(f"images/{i+1}.jpg")
    print(f"Processing (2/2) ({i+1}/{len(distusteps)})")