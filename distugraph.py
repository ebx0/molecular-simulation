from mpmath import sech
# calculate the disturbation graph of an atoms elements with its phase
# phase 1 means 1 electroni phase 2 means 2 electron in it. intermediate values means a transition

def distugraph(phase, plotsize):
    center = int(plotsize/2)
    curve = [0] * (plotsize+2)
    curve1 = [0] * (plotsize+2)
    curve2 = [0] * (plotsize+2)
    
    if phase == 1:
        for i in range(center):
            ii = int(i*2) # Only calculate half of possible area
            x = (ii-center)/center*2
            curve[ii] = int(100*(sech(2**5*x**2))) # Specific function of particle disturbation
            curve[ii+1] = curve[ii]
            
    elif phase == 2:
        for i in range(center):
            ii = int(i*2) # Only calculate half of possible area
            x = (ii-center)/center*2
            curve[ii] = int(100*(0.4*sech(3.25*x**2) - 0.45*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation
            curve[ii-1] = curve[ii]
            
    elif phase > 1 and phase < 2:
        for i in range(center):
            ii = int(i*2) # Only calculate half of possible area
            x = (ii-center)/center*2
            curve1[ii] = int(100*(sech(2**5*x**2))) # Specific function of particle disturbation 1
            curve2[ii] = int(100*(0.4*sech(3.25*x**2) - 0.45*sech(5*x**2) + sech(2**5*x**2))) # Specific function of particle disturbation 2
            curve[ii] = (curve1[ii]*(2-phase)) + (curve2[ii]*(phase-1))
            curve[ii-1] = curve[ii]
    else:
        print("Error in distugraph. Phase not avaible")
    curve = [i / 100 for i in curve]
    return curve