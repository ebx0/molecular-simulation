from PIL import Image
import numpy as np

#defined functions
from monoatomicsim import monoasim
from resizer import resize
from distugraph import distugraph

distulist = []
images = []

initial = 1 # starting phase of atom
final = 2 # final phase of atom
scale = 8 # resolution of heatmap of electrons
plotsize = 512 # size of requested plot
    
steps = 5
distusteps = []

for step in range(steps):
    phase = (initial*(1-(step/steps)) + final*((1+step)/steps))/2
    distu = distugraph(phase, plotsize) # Find the disturbation line for every stage of motion
    distusteps.append(distu) 
    
graph = []

for i in range(steps):
    graph.append(monoasim(plotsize, distusteps[i]))
    print(f"Processing (1/2) ({i+1}/{len(distusteps)})")
    
for i in range(len(graph)):
    image = (graph[i])[0]
    image2 = (graph[i])[1] # Heatmap
    field = (graph[i])[2] # Electric Field
    
    image = np.multiply(image,128) # color with 128
    
    image2 = resize(image2, plotsize)
    field = resize(field, plotsize)
            
    concat = np.concatenate((image,image2,field), axis=1)
            
    Image.fromarray(np.concatenate((concat,concat,concat), axis=2)).save(f"../images/{i+1}.jpg")
    print(f"Processing (2/2) ({i+1}/{len(distusteps)})")