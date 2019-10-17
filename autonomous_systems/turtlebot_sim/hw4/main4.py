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
for i in range(N):
    state = tbot.states[:,i]
    plotter.update_particles(tbot.states[:, i], mcl.xhat, mcl.Chi, mcl.sigma.diagonal(), i)
    # state = tbot.propagate_state(tbot.states[:,i], tbot.vc[i], tbot.omgc[i])
    z = tbot.get_measurements(tbot.states[:, i], particles=False)
    
    mcl.update(tbot.vc[i], tbot.omgc[i], z)

    # update plot animation

plotter.make_plots()