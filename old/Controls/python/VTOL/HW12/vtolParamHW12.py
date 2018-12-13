# Single link arm Parameter File
import numpy as np
import control as cnt
import sys
sys.path.append('..')  # add parent directory
import vtolParam as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal
tau_max = P.tau_max
mp = P.mp
mc = P.mc
mt = P.mt
Jc = P.Jc
g  = P.g
d  = P.d
mu = P.mu

Fe = mt * g

# State Space Equations
# xdot = A*x + B*u
# y = C*x
Alon = np.matrix([[0,1],[0,0]])
Blon = np.matrix([[0],[1/mt]])
Clon = np.matrix([1,0])

Alat = np.matrix([[0,0,1,0], [0,0,0,1], [0,-g,-mu/mt, 0], [0,0,0,0]])
Blat = np.matrix([[0],[0],[0],[1.0/(Jc + 2*mp*d**2)]])
Clat = np.matrix([[1,0,0,0], [0,1,0,0]])


# Augmented
Alon1 = np.matrix([[0,1.0,0],[0,0,0],[-1.0,0,0]])
Blon1 = np.matrix([[0],[1.0/mt],[0]])

Alat1 = np.matrix([[0,0,1.0,0,0],
                   [0,0,0,1.0,0],
                   [0,-g,-mu/mt,0,0],
                   [0,0,0,0,0],
                   [-1.0,0,0,0,0]])
Blat1 = np.matrix([[0],[0],[0],[1.0/(Jc + 2*mp*d**2)],[0]])

#  tuning parameters
tr_h =  0.2
tr_th = 0.2
tr_z = tr_th * 8
zeta = 0.707
integrator_pole_lon = -1.0
integrator_pole_lat = -1.0

# gain calculation
wn_h  = 2.2/tr_h
wn_th = 2.2/tr_th  # natural frequency
wn_z  = 2.2/tr_z
des_char_poly_lon = np.convolve([1, 2*zeta*wn_h, wn_h**2], np.poly(integrator_pole_lon))
des_poles_lon = np.roots(des_char_poly_lon)

des_char_poly_lat = np.convolve(
    np.convolve([1, 2*zeta*wn_z, wn_z**2], [1, 2*zeta*wn_th, wn_th**2]),
    np.poly(integrator_pole_lat))
des_poles_lat = np.roots(des_char_poly_lat)

# print "poles lon:",des_poles_lon
# print "poles lat:",des_poles_lat

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(Alon1, Blon1)) != 3 \
    or np.linalg.matrix_rank(cnt.ctrb(Alat1, Blat1)) != 5:
    print("The system is not controllable")
else:
    K_lon1 = cnt.acker(Alon1, Blon1, des_poles_lon)
    K_lon = np.matrix([K_lon1.item(0),K_lon1.item(1)])
    ki_lon = K_lon1.item(2)

    K_lat1 = cnt.acker(Alat1, Blat1, des_poles_lat)
    K_lat = np.matrix([K_lat1.item(0),K_lat1.item(1),K_lat1.item(2),K_lat1.item(3)])
    ki_lat = K_lat1.item(4)
    # ki_lat = 5
    print('K_lon1: ', K_lon1)
    print('ki_lon: ', ki_lon)
    print('K_lat1: ', K_lat1)
    print('ki_lat: ', ki_lat)
