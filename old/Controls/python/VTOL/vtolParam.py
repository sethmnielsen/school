# vtol Parameter File
import numpy as np

# Physical parameters known to the controller
mp = 0.25  # kg
mc = 1.0
mt = mc + 2*mp
Jc = 0.0042
d =  0.3
mu = 0.1
r =  0.16
g =  9.81

# Simulation Parameters
t_start = 0.0;  # Start time of simulation
t_end = 100.0;   # End time of simulation
Ts = 0.01      # sample time for simulation
t_plot = 0.2  # the plotting and animation is updated at this rate

# parameters for animation
w = 0.2   # width of beam in animation

# Initial Conditions
z0   = 0.0
zd0  = 0.0
h0   = 0.0
hd0  = 0.0
th0  = 0.0
thd0 = 0.0

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2.0*sigma-Ts)/(2.0*sigma+Ts)  # dirty derivative gain

# saturation limits
F_max = 100.0
tau_max = 1.5
