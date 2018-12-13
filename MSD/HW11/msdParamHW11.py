# Single link arm Parameter File
import numpy as np
import control as cnt
import sys
sys.path.append('..')  # add parent directory
import msdParam as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal
m = P.m
b = P.b
k = P.k

#  tuning parameters
tr = 1
zeta = 0.707

# State Space Equations
# xdot = A*x + B*u
# y = C*x
A = np.matrix([[0,1],
                [-k/m,-b/m]])

B = np.matrix([[0],
              [1/m]])

C = np.matrix([1,0])

# gain calculation
wn = 2.2/tr  # natural frequency
des_char_poly = [1, 2*zeta*wn, wn**2]
des_poles = np.roots(des_char_poly)
print des_poles

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A, B)) != 2:
    print("The system is not controllable")
else:
    K = cnt.acker(A, B, des_poles)
    kr = -1.0/(C[0]*np.linalg.inv(A-B*K)*B)
    print('K: ', K)
    print('kr: ', kr)
