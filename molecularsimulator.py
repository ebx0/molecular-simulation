from PIL import Image
import numpy as np
from random import random, randint

#defined functions
from monoatomicsim import monoasim
from distugraph import distugraph
from atom import atom


phase = 2
area = 512*4
plotsize = 512 # size of requested plot
scaledsize = int(plotsize / 8)

atoms = []

for i in range(10):
    atoms.append(atom([randint(100, area-100),randint(100, area-100)],[(random()-0.5)*5,(random()-0.5)*5],phase))
    
#atoms.append(atom([1,1],[20,20],phase))
#atoms.append(atom([700,700],[-20,-20],phase))

steps = 240

for i in range(steps):
    
    bg = [0,0,[0,0]]
    bg[0] = np.zeros((plotsize*8, plotsize*8, 3), dtype=np.uint8)
    bg[1] = np.zeros((plotsize, plotsize, 3), dtype=np.uint8)
    bg[2][0] = np.zeros((plotsize, plotsize, 1), dtype=np.double)
    bg[2][1] = np.zeros((plotsize, plotsize, 1), dtype=np.double)
    
    for atomv in atoms:
        try:        
            distu = distugraph(atomv.phase, plotsize)
            data = monoasim(plotsize, distu)
            
            image = data[0]
            image2 = data[1] # Heatmap
            fieldmg = data[2][0] # Electric Field magnitude
            fielddr = data[2][1] # Electric Field direction
            
            image = np.multiply(image,128) # color with 128
                
            x = int(atomv.position[0]/8) # atoms positions, starting
            y = int(atomv.position[1]/8) # atoms positions, starting
            x2 = x+scaledsize # atoms positions, finish position of array
            y2 = y+scaledsize # atoms positions, finish position of array

            bg[1][x:x2,y:y2] += data[1] # print the atom heatmap
            bg[2][0][x:x2,y:y2] += data[2][0] # hortizonal field
            bg[2][1][x:x2,y:y2] += data[2][1] # vertical field
            
        except: # If atom crush into wall, flip its velocity
            if int(atomv.position[0]/8) < scaledsize or int(atomv.position[0]/8) > area - scaledsize:
                atomv.flip([True,False])
            if int(atomv.position[1]/8) < scaledsize or int(atomv.position[1]/8) > area - scaledsize:
                atomv.flip([False,True])
            
            
        
    for atomv in atoms:
        x=int(atomv.position[0]/8)+int(scaledsize/2)
        y=int(atomv.position[1]/8)+int(scaledsize/2)
        try:
            atomv.step(1, [int(bg[2][0][x,y]*10), int(bg[2][1][x,y]*10)])
        except:
            if int(atomv.position[0]/8) > area - scaledsize:
                atomv.flip([True,False])
            if int(atomv.position[1]/8) > area - scaledsize:
                atomv.flip([False,True])
    Image.fromarray(bg[1]).save(f"../images/{i+1}.png")
    print(f"Processing ({i+1}/{steps})")