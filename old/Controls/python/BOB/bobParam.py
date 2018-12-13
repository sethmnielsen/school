
# BOB Parameter File
import numpy as np

# Physical parameters known to the controller
m1 = 0.35;  # ball
m2 = 2.0;   # beam
g = 9.81;
ell = 0.5
radius = 0.05

# Simulation Parameters
t_start = 0.0;  # Start time of simulation
t_end = 100.0;   # End time of simulation
Ts = 0.01;      # sample time for simulation
t_plot = 0.5;   # the plotting and animation is updated at this rate

# parameters for animation
w = ell    # width of beam in animation
h = 0.01   # height of beam in animation
c = 1.5

# Initial Conditions
# z0 = ell/2.0;
z0 = 0.0
zd0 = 0.0
th0 = 0.0
thd0 = 0.0

# dirty derivative parameters
sigma = 0.03  # cutoff freq for dirty derivative
beta = (2.0*sigma-Ts)/(2.0*sigma+Ts)  # dirty derivative gain

# saturation limits
th_max = 70.0*np.pi / 180.0
F_max = 100.0
