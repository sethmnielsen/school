# Single link msd Parameter File
import numpy as np
# import control as cnt
import sys
sys.path.append('..')  # add parent directory
import msdParam as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal

tr = 2.0
wn = 2.2/tr
zeta = 0.7

# PID gains
kd = (2*zeta*wn - 0.1) * 5
kp = (wn**2 - 0.6)*4.5
ki = 0.2  # integrator gain

# print('kp: ', kp)
# print('kd: ', kd)
