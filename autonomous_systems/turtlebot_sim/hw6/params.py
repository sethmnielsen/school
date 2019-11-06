import numpy as np

fov = 90
rho = 4

sz = 10

state0 = np.array([3, 0, np.pi/2])
alphas = np.array([0.1, 0.01, 0.01, 0.1])

sig_r = 0.1
sig_phi = 0.05

radius = 3
pizza_slices = 10
num_pizzas = 2
dt = 0.1

# (x – h)2 + (y – k)2 = r2, center point (h, k) and radius r
interval = np.pi/(pizza_slices/2)
angles = np.arange(0, 2*np.pi, interval)
pos = np.array([radius*np.cos(angles), radius*np.sin(angles)])
x_truth = np.array([*pos, angles])
t_arr = np.arange(0, pizza_slices*num_pizzas, dt)
N = len(t_arr)
num_lms = 5
lmarks = np.random.rand(2,num_lms) * 2*sz - sz


vc = np.ones(N) * 2
omgc = np.ones(N) * np.pi/5