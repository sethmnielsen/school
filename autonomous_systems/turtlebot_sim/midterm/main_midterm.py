#!/usr/env python3

import numpy as np
from scipy.io import loadmat
import scipy.linalg as spl

from eif_filter import EIF
from plotter_midterm import PlotterMidterm
import params as pm
from utils import wrap

np.set_printoptions(precision=3, suppress=False, sign=' ', linewidth=160)

eif = EIF()

animate = True

plotter = PlotterMidterm(animate, pm)

# Load mat_file data
mat_file = f'./midterm_data.mat'
data = loadmat(mat_file)
x_truth = data['X_tr'].squeeze()
x_truth = wrap(x_truth, 2)
t = data['t'].squeeze()
r = data['range_tr'].squeeze().T
phi = data['bearing_tr'].squeeze().T
lmarks = data['m'].squeeze()
v = data['v'].squeeze()
vc = data['v_c'].squeeze()
omg = data['om'].squeeze()
omgc = data['om_c'].squeeze()
del data

eif.marks = lmarks
eif.x_truth = x_truth

N = pm.N
for i in range(N):
    eif.prediction_step(vc[i], omgc[i])
    eif.measurement_correction(r[:,i], phi[:,i])

    eif.write_history(i)

    # update plot animation
    plotter.update_eif_plot(x_truth[:,i], eif.xhat, i)

plotter.make_plots_eif(t, eif.ksi_hist, eif.error_cov_hist)
