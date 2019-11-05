import numpy as np

state0 = np.array([3, 0, np.pi/2])
alphas = np.array([0.1, 0.01, 0.01, 0.1])

sig_r = 0.1
sig_phi = 0.05

radius = 3
pizza_slices = 100
num_pizzas = 10
dt = 0.1

# (x – h)2 + (y – k)2 = r2, center point (h, k) and radius r
interval = np.pi/(pizza_slices/2)
angles = np.arange(0, 2*np.pi, interval)
pos = np.array([radius*np.cos(angles), radius*np.sin(angles)])
x_truth = np.array([*pos, angles])
t = np.arange(0, pizza_slices*num_pizzas, dt)
N = len(t)
lmarks = np.array([[6, 4],
                   [-7, 8],
                   [6, -4]]).T

vc = np.ones(N) * 2
omgc = np.ones(N) * np.pi/5