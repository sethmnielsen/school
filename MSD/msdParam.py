# Mass Spring Damper Parameter File
import numpy as np

# Physical parameters known to the controller
m = 5.0;  # kg
k = 3.0; # N/m
b = 0.5; # N m s

# Simulation Parameters
t_start = 0.0;  # Start time of simulation
t_end = 25.0;   # End time of simulation
Ts = 0.01;      # sample time for simulation
t_plot = 0.1;   # the plotting and animation is updated at this rate

# parameters for animation
w = 4.0   # width of mass in animation
h = 4.0   # height of mass in animation
c = 1.5

# Initial Conditions
z0 = 0.0;
zd0 = 1.0;

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2.0*sigma-Ts)/(2.0*sigma+Ts)  # dirty derivative gain

# saturation limits
F_max = 10.00001                # Max force, N
