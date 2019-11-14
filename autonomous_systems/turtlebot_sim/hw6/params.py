import shared
if shared.USE_CUPY:
    import cupy as xp
else:
    import numpy as xp

import numpy as np


## NUMPY OR CUPY SPECIFIC ARRAYS
num_lms = 100
sz = 12
center = 5
state0 = xp.array([0, 0, 0])
alphas = xp.array([0.1, 0.01, 0.01, 0.1])

m = sz*0.8
lmarks = xp.random.rand(2,num_lms) * 2*m - m
lmarks[1] += center

N = 300
vc = xp.ones(N) * 2
omgc = xp.ones(N) * xp.pi/10


## OTHER VARIABLES

fov = np.radians(45)
rho = 8 

sig_r = 0.1
sig_phi = 0.05

dt = 0.1
t_arr = np.arange(0, N//dt, dt)
