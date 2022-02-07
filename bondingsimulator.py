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
    
steps = 20
distusteps = []

for step in range(steps+1):
    phase = initial*(1-(step/steps)) + final*(step/steps)
    distu = distugraph(phase, plotsize) # Find the disturbation line for every stage of motion
    distusteps.append(distu) 
    
graph = []

for i in range(steps):
    graph.append(monoasim(plotsize, distusteps[i]))
    print(f"Processing (1/2) ({i+1}/{len(distusteps)-1})")
    
for i in range(len(graph)):
    image = (graph[i])[0]
    image2 = (graph[i])[1] # Heatmap
    fieldx = (graph[i])[2][0] # Electric Field magnitude
    fieldy = (graph[i])[2][1] # Electric Field direction
    
    image = np.multiply(image,128) # color with 128
    
    image2 = resize(image2, plotsize)
    fieldx = resize(fieldy, plotsize)
    fieldy = resize(fieldy, plotsize)
            
    concat = np.concatenate((image,image2,fieldx,fieldy), axis=1)
            
    Image.fromarray(np.concatenate((concat,concat,concat), axis=2)).save(f"../images/{i+1}.png")
    print(f"Processing (2/2) ({i+1}/{len(distusteps)-1})")