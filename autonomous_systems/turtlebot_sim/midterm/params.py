import numpy as np

dt = 0.1

sz = 30
x0 = -5
y0 = 0
th0 = np.pi/2
state0 = [x0, y0, th0]

t_end = 30
N = int(t_end / dt + 1)

# noise 
sig_r = 0.2 # [m]
sig_phi = 0.1 # [rad]
sigs = np.array([sig_r, sig_phi])
R = np.diag(sigs)**2

# velocity motion model noise params
sig_v = 0.15 # m/s
sig_omg = 0.1 # rad/s

lmarks = np.array([[  6, 4],
                   [ -7, 8],
                   [ 12,-8],
                   [ -2, 0],
                   [-10, 2],
                   [ 13, 7]]).T
# lmarks = np.array([[6],
                #    [4]])
num_lms = lmarks.shape[1]