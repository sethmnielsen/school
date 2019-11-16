import numpy as np
import cupy as cp

num_lms = 10
fov = np.radians(360)
rho = 20
sz = 12

center = 5

state0 = cp.array([0, 0, 0])
alphas = cp.array([0.2, 0.02, 0.02, 0.2])

sig_r = 0.1
sig_phi = 0.05

radius = 5
circumference_points = 10
num_circles = 3
dt = 0.1

t_arr = np.arange(0, circumference_points*num_circles, dt)
N = len(t_arr)
m = sz*0.8
lmarks = cp.random.rand(2,num_lms) * 2*m - m
lmarks[1] += center


vc = cp.ones(N) * 2
omgc = cp.ones(N) * np.pi/8