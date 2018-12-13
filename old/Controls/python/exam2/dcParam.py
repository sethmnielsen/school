# BOB Parameter File
import numpy as np

# Physical parameters known to the controller
J = 0.096852
b = 0.105231
k = 822.0
R = 120000.0
L = 0.0825

# Simulation Parameters
t_start = 0.0;  # Start time of simulation
t_end = 1.0;   # End time of simulation
Ts = 1e-6;      # sample time for simulation
t_plot = 1e-3;   # the plotting and animation is updated at this rate

# Initial Conditions
i0 = 0.0
th0 = 20.0*np.pi/180.0
thd0 = 0.0

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2.0*sigma-Ts)/(2.0*sigma+Ts)  # dirty derivative gain

# saturation limits
V_max = 10000.0
