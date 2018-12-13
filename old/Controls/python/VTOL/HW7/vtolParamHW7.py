# Inverted vtol Parameter File
import numpy as np
# import control as cnt
import sys
sys.path.append('..')  # add parent directory
import vtolParam as P

# sample rate of the controller
Ts = P.Ts

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2 * sigma - Ts) / (2 * sigma + Ts)  # dirty derivative gain

####################################################
#       PD Control: Time Design Strategy
####################################################

#---------------------------------------------------
#                    Longitudinal (h)
#---------------------------------------------------

# tuning parameters
tr_h = 8.0           # Rise time for inner loop (theta)
zeta = 0.707       # Damping Coefficient for inner loop (theta)
M = 20.0              # Time scale separation between inner and outer loop
wn_h = 2.2/tr_h

# saturation limits
F_max = 100.0                   # Max Force, N
error_max = 1.0        		  # Max step size,m
theta_max = 70.0*np.pi/180.0  # Max theta, rads
h_max = 6

kp_h = P.mt * wn_h**2
kd_h = P.mt * 2*zeta*wn_h

#---------------------------------------------------
#                    Inner Loop (theta)
#---------------------------------------------------
tr_th = 1

# compute gains
kp_th = 0
kd_th = 0

DC_gain = 1.0

#---------------------------------------------------
#                    Outer Loop (zv)
#---------------------------------------------------
# coefficients for desired outer loop
tr_z = M*tr_th  # desired rise time, s
wn_z = 2.2/tr_z  # desired natural frequency

# compute gains
kp_z = -0.00493
kd_z = -0.0317
