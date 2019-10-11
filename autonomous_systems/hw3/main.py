#!/usr/env python3

import sys
import numpy as np
from scipy.io import loadmat

from plotter import Plotter
from turtlebot import Turtlebot
from ukf_filter import UKF
from utils import wrap


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
    # state_hist = np.zeros((N, 3))
    # xhat_hist = np.zeros((N, 3))
    # est_err_hist = np.zeros((N, 3))
    # err_cov_hist = np.zeros((N, 3))
    
    for i in range(1, N):
        turtle.propagate_truth(i)

        zt = turtle.get_measurements()
        K = ukf.update(zt, turtle.vc[i], turtle.omgc[i])

        # plotty plotty plot plot
        # update plot animation
        plotter.update(turtle.state, ukf.xhat, ukf.Sigma.diagonal(), i)

        # append to plotting variable histories
        # state, xhat, err, x_cov, y_cov, th_cov, K
        # state_hist[i] = turtle.state
        # xhat_hist[i] = ukf.xhat
        # est_err_hist[i] = ukf.xhat - turtle.state
        # err_cov_hist[i] = ukf.Sigma.diagonal()

    plotter.make_plots()

