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

#  tuning parameters
tr = 0.015
zeta = 0.707

# gain calculation
wn = 2.2/tr  # natural frequency
des_char_poly = [1, 2*zeta*wn, wn**2]
poles = np.roots(des_char_poly)
p3 = np.real(poles[0])
des_poles = np.array([poles[0], poles[1], p3*2])
print "Poles = ", des_poles
# print des_poles.shape
# print "A = ",A
# print A.shape
# print "B = ",B
# print B.shape

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A, B)) != 2:
    print("The system is not controllable")
else:
    K = cnt.place(A, B, des_poles)
    kr = -1.0/(C[0]*np.linalg.inv(A-B*K)*B)
    print('K: ', K)
    print('kr: ', kr)
