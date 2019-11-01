#!/usr/env python3

'''
The state_meas_data.mat file includes three variables:

    - X: state vector holding (x, y, theta) at each time step
    - z: measurement vector holding (range, bearing) for eleven laser range finder measurements at each time step. NaN is reported if a "hit" is not detected.
    - thk: vector of eleven range finder pointing angles ranging between -pi/2 (-90 deg) and pi/2 (90 deg). Pointing angles are equally spaced at pi/10 rad (22.5 deg) of separation. 
Use the following parameters for your inverse range sensor model: alpha = 1 m, beta = 5 deg, z_max = 150 m.
'''

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


    

    # update plot animation
    # plotter.update_mcl_plot(state, mcl.xhat, mcl.Chi, mcl.P.diagonal(), i)

    # z = tbot.get_measurements(state, particles=False)
    # mcl.update(tbot.vc[i], tbot.omgc[i], z)


