# Single link arm Parameter File
import numpy as np
import control as cnt
import sys
sys.path.append('..')  # add parent directory
import bobParam as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal
m1 = P.m1
m2 = P.m2
g  = P.g
l  = P.ell
ze = l/2.0
den = (m1*ze**2 + m2*l**2 / 3.0)

# State Space Equations
# xdot = A*x + B*u
# y = C*x
A = np.matrix([[0,0,1.0,0],[0,0,0,1.0],[0,-9.81,0,0],[-m1*g/den,0,0,0]])
B = np.matrix([[0],[0],[0],[l/den]])
C = np.matrix([[1.0,0,0,0],[0,1.0,0,0]])

#  tuning parameters
tr_th = 0.1
tr_z = tr_th * 6.5
zeta = 0.707

# gain calculation
wn_th = 2.2/tr_th  # natural frequency
wn_z  = 2.2/tr_z
des_char_poly = np.convolve([1, 2*zeta*wn_z, wn_z**2], [1, 2*zeta*wn_th, wn_th**2])
des_poles = np.roots(des_char_poly)
print des_poles

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A, B)) != 4:
    print("The system is not controllable")
else:
    K = cnt.place(A, B, des_poles)
    kr = -1.0/(C[0]*np.linalg.inv(A-B*K)*B)
    print('K: ', K)
    print('kr: ', kr)
