#!/usr/env python3

import sys
sys.path.append('..')
import numpy as np
from scipy.io import loadmat

from mcl_filter import MCL
from plotter import Plotter
from turtlebot import Turtlebot
from utils import wrap
import params as pm

np.set_printoptions(precision=3, suppress=False, sign=' ', linewidth=160)

tbot = Turtlebot()
mcl = MCL(tbot)
plotter = Plotter()

# Parse cmd line args
args = sys.argv[1:]
if len(args) == 0: # Compute truth ourselves
    tbot.build_vel_arrays()
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
    # tbot.pass_matlab_data()


N = tbot.N
state_hist = np.zeros((3,N))
state_hist[:,0] = pm.state0
Chi = np.zeros((3, pm.M))
for i in range(1, N):
    state = tbot.sample_motion_model(tbot.vc[i], tbot.omgc[i], tbot.states[:,i])
    z = tbot.get_measurements(state, particle=False)
    
    Chi = mcl.update(tbot.vc[i], tbot.omgc[i], z)

    # append to plotting variable histories
    state_hist[:,i] = state

    # update plot animation
    # plotter.update_particle(state_hist[:i], Chi)

plotter.make_plots()