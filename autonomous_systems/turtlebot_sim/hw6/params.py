import numpy as np

fov = 90
rho = 4

sz = 12

state0 = np.array([0, 0, 0])
alphas = np.array([0.1, 0.01, 0.01, 0.1]) * 0.0001

sig_r = 0.1 * 0.01
sig_phi = 0.05 * 0.01

radius = 3
circumference_points = 10
num_circles = 2
dt = 0.1

# (x – h)2 + (y – k)2 = r2, center point (h, k) and radius r
# interval = np.pi/(circumference_points/2)
# angles = np.arange(0, 2*np.pi, interval)
# pos = np.array([radius*np.cos(angles), radius*np.sin(angles)])
# x_truth = np.array([*pos, angles])
t_arr = np.arange(0, circumference_points*num_circles, dt)
N = len(t_arr)
num_lms = 10
m = sz*0.8
lmarks = np.random.rand(2,num_lms) * 2*m - m


vc = np.ones(N) * 2
omgc = np.ones(N) * np.pi/5