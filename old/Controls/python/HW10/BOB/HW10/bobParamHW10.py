# Inverted bob Parameter File
import numpy as np
# import control as cnt
import sys
sys.path.append('..')  # add parent directory
import bobParam as P

# sample rate of the controller
Ts = P.Ts

# dirty derivative parameters
sigma = 0.05  # cutoff freq for dirty derivative
beta = (2 * sigma - Ts) / (2 * sigma + Ts)  # dirty derivative gain

####################################################
#       PD Control: Time Design Strategy
####################################################
# tuning parameters
tr_th = 0.153          # Rise time for inner loop (theta)
zeta = 0.707       # Damping Coefficient for inner loop (theta)
M = 10              # Time scale separation between inner and outer loop

# saturation limits
F_max = 100.0                   # Max Force, N
error_max = 100.0        		  # Max step size,m
theta_max = 70.0*np.pi/180.0  # Max theta, rads

#---------------------------------------------------
#                    Inner Loop
#---------------------------------------------------
# parameters of the open loop transfer function
wn_th = 2.2/tr_th

# compute gains
kp_th = wn_th**2 * P.ell * (P.m1/4.0 + P.m2/3.0)
kd_th = 2*zeta*wn_th*P.ell * (P.m1/4.0 + P.m2/3.0)
print "kp_th =",kp_th
print "kd_th =",kd_th
ki_th = 0.1

DC_gain = 1.0

#---------------------------------------------------
#                    Outer Loop
#---------------------------------------------------
# coefficients for desired outer loop
tr_z = M*tr_th  # desired rise time, s
wn_z = 2.2/tr_z # desired natural frequency

# compute gains
kp_z = -(1/P.g) * wn_z**2
kd_z = -(2/P.g) * zeta * wn_z
ki_z = -0.05
print "kp_z =",kp_z
print "kd_z =",kd_z
