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
A = np.matrix([[0.0, 0.0, 1.0, 0.0],
               [0.0, 0.0, 0.0, 1.0],
               [0.0,  -g, 0.0, 0.0],
               [-m1*g/den,0.0, 0.0, 0.0]])

B = np.matrix([[0],[0],[0],[l/den]])
C = np.matrix([[1.0,0,0,0],[0,1.0,0,0]])

A1= np.matrix([[0.0, 0.0, 1.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 1.0, 0.0],
               [0.0,  -g, 0.0, 0.0, 0.0],
               [-m1*g/den,0.0, 0.0, 0.0, 0.0],
               [-1.0, 0.0, 0.0, 0.0, 0.0]])
B1 = np.matrix([[0],[0],[0],[l/den],[0]])

#  tuning parameters
tr_th = 0.13
tr_z = tr_th * 10.0
zeta = 0.707
integrator_pole = -0.1  # integrator pole

# gain calculation
wn_th = 2.2/tr_th  # natural frequency
wn_z  = 2.2/tr_z
des_char_poly = np.convolve(
    np.convolve([1, 2*zeta*wn_z, wn_z**2], [1, 2*zeta*wn_th, wn_th**2]),
    np.poly(integrator_pole))
des_poles = np.roots(des_char_poly)
print des_poles

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 5:
    print("The system is not controllable")
else:
    K1 = cnt.acker(A1, B1, des_poles)
    K = np.matrix([K1.item(0), K1.item(1), K1.item(2), K1.item(3)])
    ki = K1.item(4)
    print('K: ', K)
    print('ki: ', ki)
