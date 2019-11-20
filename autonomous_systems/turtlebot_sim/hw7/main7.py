#!/usr/env python3

import sys
import shared
import chainer as ch

if __name__ == '__main__':
    if ch.cuda.available and '--gpu' in sys.argv:
        shared.USE_CUPY = True
        import cupy as xp
    else:
        shared.USE_CUPY = False
        import numpy as xp
        xp.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=120)

    from fast_slam import Fast_SLAM
    import params as pm
    import turtlebot
    from plotter import Plotter
    from utils import wrap


    # ------------------------ INITIALIZATION ----------------------------#

    tbot = turtlebot.Turtlebot(pm, pm.vc, pm.omgc)
    tbot.states[:,0] = pm.state0
    fslam = Fast_SLAM(pm, tbot)

    animate = True

    plotter = Plotter(animate, pm)

    finished = False
    N = pm.N


    # ------------------------ BEGIN MAIN LOOP ----------------------------#
    
    
    for i in range(1,N):              # i is timestep
        for j in range(pm.num_lms):   # j is landmark index
            state = tbot.states[:,i]  # true state

            fslam.prediction_step(tbot.vc[i-1], tbot.omgc[i-1], j) # propagate all particles forward
            
            z, detected_mask = tbot.get_measurements(state)
            if xp.any(detected_mask):
                fslam.measurement_correction(z, detected_mask)