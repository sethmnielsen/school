# Single link arm Parameter File
import numpy as np
import control as cnt
import sys
sys.path.append('..')  # add parent directory
import dcParam as P

np.set_printoptions(precision=2, suppress=True)


Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
V_max = P.V_max
R = P.R
L = P.L
J = P.J
k = P.k
b = P.b

# State Space Equations
# xdot = A*x + B*u
# y = C*x
A = np.matrix([[0.0,  0.0,  1.0],
               [0.0, -R/L, -k/L],
               [0.0,  k/J, -b/J]])
B = np.matrix([[0],[1/L],[0]])
C = np.matrix([1.0,0,0])

A1= np.matrix([[0.0,  0.0,  1.0, 0],
               [0.0, -R/L, -k/L, 0],
               [0.0,  k/J, -b/J, 0],
               [-1.0,   0,    0, 0]])
B1= np.matrix([[0],[1/L],[0],[0]])

#  tuning parameters
tr = 0.015
zeta = 0.707

# gain calculation
# wn = 2.2/tr  # natural frequency
# des_char_poly = [1, 2*zeta*wn, wn**2]
# poles = np.roots(des_char_poly)
p1 = -127 + 50j
p2 = -127 - 50j
p3 = -150
p4 = -212
des_poles = np.array([p1, p2, p3, p4])
print "Poles = ", des_poles
# print des_poles.shape
# print "A = ",A
# print A.shape
# print "B = ",B
# print B.shape

# Compute the gains if the system is controllable
# if np.linalg.matrix_rank(cnt.ctrb(A, B)) != 2:
    # print("The system is not controllable")
# else:
K1 = cnt.acker(A1, B1, des_poles)
K = np.matrix([K1.item(0), K1.item(1), K1.item(2)])
ki = K1.item(3)
print('K: ', K)
print('ki: ', ki)
