import numpy as np

dt = 0.1

sz = 20
x0 = -5
y0 = -3
th0 = np.pi/2

t_arr = np.arange(0, 20, dt)

# Robot physical constants    
bot_radius = 0.5
bot_body_heading = np.array([bot_radius, 0])
poly_res = 12
bot_body_alpha = 0.4

# noise 
sig_r = 0.1 # [m]
sig_phi = 0.05 # [rad]
sigs = np.array([sig_r, sig_phi])
Q = np.diag(sigs)**2

# velocity motion model noise params
vm_alphas = np.array([0.1, 0.01, 0.01, 0.1])

lmarks = np.array([[6, 4],
                   [-7, 8],
                   [6, -4]]).T
# lmarks = np.array([[6],
#                    [4]])
num_lms = lmarks.shape[1]

ndim = 7