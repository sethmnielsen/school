# MSD2 Parameter File
import numpy as np

# Physical parameters known to the controller
m1 = 2500.0;   # kg
m2 = 320.0;    # kg
k1 = 80000.0;  # N/m
k2 = 500000.0; # N/m
b1 = 350.0;    # N-s/m
b2 = 15020.0;  # N-s/m

# Simulation Parameters
t_start = 0.0;  # Start time of simulation
t_end = 60.0;   # End time of simulation
Ts = 0.01;      # sample time for simulation
t_plot = 0.4;   # the plotting and animation is updated at this rate

# Initial Conditions
x10 = 0.0
x20 = 0.0
x30 = 1.0
x40 = 0.0

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2.0*sigma-Ts)/(2.0*sigma+Ts)  # dirty derivative gain

# saturation limits
F_max = 1000.0
