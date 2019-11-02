#!/usr/env python3

import sys
sys.path.append('..')
import numpy as np
from scipy.io import loadmat

from eif_filter import EIF
from plotter import Plotter
from turtlebot import Turtlebot
from utils import wrap
import params as pm

np.set_printoptions(precision=3, suppress=False, sign=' ', linewidth=160)

tbot = Turtlebot()
eif = EIF()

animate = True

plotter = Plotter(animate)

# Load mat_file data
mat_file = f'ukf_data_{args[0]}.mat'
data = loadmat(mat_file)
x_state = data['X_tr'].flatten()
phi = data['bearing_tr'].flatten()
th = data['th'].flatten()
v = data['v'].flatten()
x = data['x'].flatten()
y = data['y'].flatten()
del data
# tbot.pass_matlab_data()


N = tbot.N
for i in range(N):
    state = tbot.states[:,i]

    # update plot animation
    plotter.update_mcl_plot(state, mcl.xhat, mcl.Chi, mcl.P.diagonal(), i)

    z = tbot.get_measurements(state, particles=False)
    mcl.update(tbot.vc[i], tbot.omgc[i], z)

plotter.make_plots()