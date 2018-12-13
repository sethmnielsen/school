# Single link arm Parameter File
import numpy as np
# import control as cnt
import sys
sys.path.append('..')  # add parent directory
import msdParam as P


#  tuning parameters
tr = 0.55
zeta = 0.707
integrator_pole = -0.7
tr_obs = 0.1
wn_obs = 2.2/tr_obs  # natural frequency for observer
zeta_obs = 0.707  # damping ratio for observer

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal
m = P.m
b = P.b
k = P.k

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

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != 3:
    print("The system is not controllable")
else:
    K1 = cnt.acker(A1, B1, des_poles)
    K  = np.matrix([K1.item(0), K1.item(1)])
    ki = K1.item(2)

# observer design
des_obs_char_poly = [1, 2*zeta_obs*wn_obs, wn_obs**2]
des_obs_poles = np.roots(des_obs_char_poly)

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(A.T, C.T)) != 2:
    print("The system is not observerable")
else:
    L = cnt.acker(A.T, C.T, des_obs_poles).T

print('K: ', K)
print('ki: ', ki)
print('L^T: ', L.T)
