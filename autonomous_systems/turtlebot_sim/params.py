import numpy as np

dt = 0.1

sz = 20
x0 = -5
y0 = -3
th0 = np.pi/2
state0 = [x0, y0, th0]

t_arr = np.arange(0, 20, dt)

# noise 
sig_r = 0.1 # [m]
sig_phi = 0.05 # [rad]
sigs = np.array([sig_r, sig_phi])
Q = np.diag(sigs)**2

# velocity motion model noise params
alphas = np.array([0.1, 0.01, 0.01, 0.1])

lmarks = np.array([[6, 4],
                   [-7, 8],
                   [6, -4]]).T
# lmarks = np.array([[6],
                #    [4]])
num_lms = lmarks.shape[1]

# UKF
ndim = 7

# Particle Filter
M = 1000