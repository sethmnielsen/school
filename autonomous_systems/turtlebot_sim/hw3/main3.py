#!/usr/env python3

import sys
sys.path.append('..')
import numpy as np
from scipy.io import loadmat

from plotter import Plotter
from turtlebot import Turtlebot
from hw3.ukf_filter import UKF
import params as pm

np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=160)

if __name__ == '__main__':
    turtle = Turtlebot()
    ukf = UKF()
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


    # Histories
    N = turtle.N
    for i in range(1, N):
        zt = turtle.get_measurements(turtle.states[i])
        K = ukf.update(zt, turtle.vc[i], turtle.omgc[i])

        # plotty plotty plot plot
        # update plot animation
        plotter.update_kalman_plot(turtle.states[i], ukf.xhat, ukf.Sigma.diagonal(), i)

    plotter.make_plots()

