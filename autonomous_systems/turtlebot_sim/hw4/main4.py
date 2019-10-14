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

# if __name__ == '__main__':
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
for i in range(1, N):
    state = turtle.sample_motion_model(turtle.vc[i], turtle.omgc[i], turtle.state_t)

    zt = turtle.get_measurements()
    mcl.update(turtle.vc[i], turtle.omgc[i], zt)

    # update plot animation
    plotter.update(turtle.state, mcl.xhat, mcl.Sigma.diagonal(), i)

    # append to plotting variable histories

plotter.make_plots()

