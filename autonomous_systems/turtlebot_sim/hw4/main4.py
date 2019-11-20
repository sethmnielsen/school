#!/usr/env python3
import sys
sys.path.append('..')
import numpy as np
np.set_printoptions(precision=3, suppress=False, sign=' ', linewidth=120)
from scipy.io import loadmat

from mcl_filter import MCL
from plotter import Plotter
from turtlebot import Turtlebot
from utils import wrap
import params as pm


# ------------------------ INITIALIZATION ----------------------------#

animate = True
plotter = Plotter(animate)

tbot = Turtlebot()
tbot.build_vel_and_state()
mcl = MCL(tbot)

N = tbot.N


# ------------------------ BEGIN MAIN LOOP ----------------------------#
for i in range(N):
    # update plot animation
    state = tbot.states[:,i]
    plotter.update_mcl_plot(state, mcl.xhat, mcl.Chi, mcl.P.diagonal(), i)

    # algorithm
    z = tbot.get_measurements(state, particles=False)
    mcl.update(tbot.vc[i], tbot.omgc[i], z)

plotter.make_plots()