#!/usr/env python3

import sys
sys.path.append('..')
import numpy as np
from scipy.io import loadmat

from hw4.mcl_filter import MCL
from plotter import Plotter
from turtlebot import Turtlebot
from utils import wrap
import params as pm



turtle = Turtlebot()
mcl = MCL()
plotter = Plotter()

# Parse cmd line args
args = sys.argv[1:]
if len(args) == 0: # Compute truth ourselves
    turtle.build_vel_arrays()
elif len(args) == 1 and args[0] in [1, 4, 5]:
    # Load mat_file data
    mat_file = f'ukf_data_{args[0]}.mat'
    data = loadmat(mat_file)
    omg = data['om'].flatten()
    t = data['t'].flatten()
    th = data['th'].flatten()
    v = data['v'].flatten()
    x = data['x'].flatten()
    y = data['y'].flatten()
    del data
    # turtle.pass_matlab_data()


N = turtle.N
state_hist = np.zeros((N, 3))
state_hist[0] = pm.state0
Chi = np.zeros((pm.M, 3))
for i in range(1, N):
    state = turtle.sample_motion_model(turtle.vc[i], turtle.omgc[i], turtle.states[i])
    z = turtle.get_measurements(state)
    
    Chi = mcl.update(turtle.vc[i], turtle.omgc[i], z)

    # append to plotting variable histories
    state_hist[i] = state

    # update plot animation
    plotter.update_particle(state_hist[:i], Chi)

plotter.make_plots()

