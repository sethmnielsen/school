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
integrator_pole = -2

#  tuning parameters
tr = 1.5
zeta = 0.707

# State Space Equations
# xdot = A*x + B*u
# y = C*x
A = np.matrix([[0.0,1.0],
                [-k/m,-b/m]])

B = np.matrix([[0],
              [1.0/m]])

C = np.matrix([1,0])

# augmented system
A1 = np.matrix([[0.0, 1.0, 0.0],
                [-k/m,-b/m, 0.0],
                [-1.0, 0.0, 0.0]])

B1 = np.matrix([[0.0],
              [1.0/m],
              [0.0]])

# gain calculation
wn = 2.2/tr  # natural frequency
des_char_poly = np.convolve([1, 2*zeta*wn, wn**2], np.poly(integrator_pole))
des_poles = np.roots(des_char_poly)
print "Poles = ", des_poles
print des_poles.shape
print "A1 = ",A1
print A.shape
print "B1 = ",B1
print B.shape

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 3:
    print("The system is not controllable")
else:
    K1 = cnt.acker(A1, B1, des_poles)
    K  = np.matrix([K1.item(0), K1.item(1)])
    ki = K1.item(2)
    print('K: ', K)
    print('ki: ', ki)
