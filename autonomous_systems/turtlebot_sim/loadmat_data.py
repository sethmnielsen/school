import numpy as np
from scipy.io import loadmat

data = loadmat('./matlab_data/state_meas_data.mat')
X = data['X']
z = data['z']
thk = data['thk']

z_r, z_phi = z
