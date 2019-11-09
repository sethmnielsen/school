#!/usr/env python3

import sys
import numpy as np
import scipy.linalg as spl

from ekf_slam import EKF_SLAM
import params as pm
from turtlebot import Turtlebot
from plotter import Plotter
from utils import wrap

np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=160)

ekfs = EKF_SLAM(pm)
tbot = Turtlebot(pm, pm.vc, pm.omgc)
tbot.states[:,0] = pm.state0

animate = True

plotter = Plotter(animate, pm)

finished = False
N = pm.N
for i in range(1,N):
    # i is my timestep
    state = tbot.states[:,i]
    
    ekfs.prediction_step(tbot.vc[i-1], tbot.omgc[i-1])
    z, lmarks_detected = tbot.get_measurements(state)
    ekfs.measurement_correction(z[0], z[1], lmarks_detected)

    ekfs.write_history(i)

    # update plot animation
    try:
        plotter.update_ekfs_plot(state, ekfs.xhat, ekfs.Pa.diagonal()[3:], i)
    except KeyboardInterrupt:
        break

    if i == N-1:
        finished = True

if finished:
    plotter.make_plots_ekfs(pm.t_arr)