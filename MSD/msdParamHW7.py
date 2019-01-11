# Single link msd Parameter File
import numpy as np
# import control as cnt
import sys
import msdParam as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal

tr = 2.7
wn = 2.2/tr
zeta = 0.7

# PD gains
kd = (2*zeta*wn - 0.1) * 5
kp = (wn**2 - 0.6)*4.5
ki = 0.0001

# print('kp: ', kp)
# print('kd: ', kd)
