# Single link arm Parameter File
import numpy as np
from scipy import signal
import control as cnt
import sys
sys.path.append('..')  # add parent directory
import msd2Param as P

np.set_printoptions(suppress=True)

#  tuning parameters
tr = 1.0
tr_x1 = tr
tr_obs = 0.1
tr_obs_x1 = tr_obs
zeta = 0.707
integrator_pole = -1.0  # integrator pole

wn = 2.2/tr  # natural frequency
wn_x1 = 2.2/tr_x1
wn_obs = 2.2/tr_obs
wn_x1_obs = 2.2/tr_obs_x1

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal
m1 = P.m1
m2 = P.m2
k1 = P.k1
k2 = P.k2
b1 = P.b1
b2 = P.b2

# State Space Equations
# xdot = A*x + B*u
# y = C*x

A = np.matrix([[0.0,              1.0,  0.0,                                          0.0    ],
               [-(b1*b2)/(m1*m2), 0.0,  ((b1/m1)*((b1/m1)+(b1/m2)+(b2/m2)))-(k1/m1), -(b1/m1)],
               [b2/m2,            0.0, -((b1/m1)+(b1/m2)+(b2/m2)),                    1.0    ],
               [k2/m2,            0.0, -((k1/m1)+(k1/m2)+(k2/m2)),                    0.0    ]])

B = np.matrix([[0],[1.0/m1],[0],[(1.0/m1) + (1.0/m2)]])
C = np.matrix([[1.0, 0,   0,     0],
               [0  , 0,   1.0,   0]])

X0 = np.zeros((5,1))
A1 = np.hstack(( np.vstack((A,-C[1])), X0 ))
B1 = np.vstack((B, 0.))


des_char_poly = np.convolve(np.convolve([1, 2*zeta*wn_x1, wn_x1**2], [1, 2*zeta*wn, wn**2]),
                            np.poly(integrator_pole))
des_poles = np.roots(des_char_poly)

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 5:
    print("The system is not controllable")
else:
    K1 = cnt.acker(A1, B1, des_poles)
    K = np.matrix([K1.item(0), K1.item(1), K1.item(2), K1.item(3)])
    ki = K1.item(4)
    print('K: ', K)
    print('ki: ', ki)

# observer design
des_obs_char_poly = np.convolve([1, 2*zeta*wn_x1_obs, wn_x1_obs**2], [1, 2*zeta*wn_obs, wn_obs**2])
des_obs_poles = np.roots(des_obs_char_poly)

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A.T, C.T)) != 4:
    print("The system is not observerable")
else:
    # L = cnt.acker(A.T, C.T, des_obs_poles).T
    L = signal.place_poles(A.T, C.T, des_obs_poles).gain_matrix.T
    print('L^T: ', L.T)
