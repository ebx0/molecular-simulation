from mpmath import sech
from monoatomicsim import monoasim
import numpy as np

distulist = []
images = []

for j in range(2):
    plotsize = 1024
    center = int(plotsize/2)
    size = 0.8
    
    distuscale = 10**2
    distu = [0] * plotsize
    
    for i in range(int(plotsize/2)):
        ii = int(i*2) # Only calculate half of possible area, for performance improvement
        x = (ii-center)/center/(size/3)
        if j == 0: 
            functionvalue = int(distuscale*(0.4*sech(2*x**2) - 0.4*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation
        if j == 1:
            functionvalue = int(distuscale*(sech(2**5*x**3))) # Specific function of particle disturbation
        distu[ii:ii+1] = [functionvalue,functionvalue]
    distulist.append(distu)
    
steps = 48
distusteps = []
for i in range(48):
    distusteps.append(distulist[0])
    
for step in range(steps):
    distusteps.append(list(np.add( np.multiply(distulist[1],(step/steps)) , np.multiply(distulist[0],(1-(step/steps))) ).astype("int")))

for i in range(48):
    distusteps.append(distulist[-1])

for i in range(len(distusteps)):
    (monoasim(plotsize, center, size, distusteps[i])).save(f"images/{i+1}.jpg")
    print(f"Processing ({i+1}/{len(distusteps)})")
