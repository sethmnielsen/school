import shared
if shared.USE_CUPY:
    import cupy as xp
else:
    import numpy as xp

import numpy as np


## NUMPY OR CUPY SPECIFIC ARRAYS
num_lms = 3
sz = 12
center = 5
state0 = xp.array([0, 0, 0])
alphas = np.array([0.1, 0.01, 0.01, 0.1, 0.01, 0.01])

m = sz*0.8
# lmarks = xp.random.rand(2,num_lms) * 2*m - m
# lmarks[1] += center
lmarks = np.array([[7, 4],
                   [-7, 8],
                   [5, -4]]).T
t_end = 30
dt = 0.05
N = int(t_end/dt)
vc = xp.ones(N) * 2
omgc = xp.ones(N) * xp.pi/10


## OTHER VARIABLES

fov = np.radians(360)
rho = 20 

sig_r = 0.1
sig_phi = 0.05

t_arr = np.arange(0, t_end, dt)


# Particles
M = 100