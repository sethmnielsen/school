#!/usr/env python3

import numpy as np
import scipy.linalg as spl

from ekf_slam import EKF_SLAM
from turtlebot import Turtlebot
from plotter import Plotter
import params as pm
from utils import wrap

np.set_printoptions(precision=3, suppress=False, sign=' ', linewidth=160)

ekfs = ekf_slam()
tbot = Turtlebot(pm, pm.vc, pm.omgc)

animate = True

plotter = Plotter(animate)

ekfs.marks = lmarks
ekfs.x_truth = x_truth

N = pm.N
for i in range(N):
    ekfs.prediction_step(tbot.vc[i], tbot.omgc[i])
    ekfs.measurement_correction(r[:,i], phi[:,i])

    ekfs.write_history(i)

    # update plot animation
    plotter.update_eif_plot(x_truth[:,i], ekfs.xhat, i)

plotter.make_plots_eif(t, ekfs.ksi_hist, ekfs.error_cov_hist)

import sys
sys.path.append('..')
import numpy as np
from scipy.io import loadmat

from utils import wrap
import hw5.params as pm

from pyqtgraph.Qt import QtCore, QtGui
from hw5.turtlebot_app import App, TurtleApp

np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=160)

mat_file = 'matlab_data/state_meas_data.mat'
data = loadmat(mat_file)
X = data['X']  # (3, 759)
z = data['z']  # (2, 11, 759)
thk = data['thk'].flatten()  # (11)
del data

z[np.isnan(z)] = np.inf
z_r, z_phi = z

app = QtGui.QApplication(sys.argv)
thisapp = App(X, z, thk)
thisapp.show()
sys.exit(app.exec_())
