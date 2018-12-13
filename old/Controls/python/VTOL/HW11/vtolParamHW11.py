# Single link arm Parameter File
import numpy as np
import control as cnt
import sys
sys.path.append('..')  # add parent directory
import vtolParam as P

Ts = P.Ts  # sample rate of the controller
beta = P.beta  # dirty derivative gain
F_max = P.F_max  # limit on control signal
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

Alat = np.matrix([[0,0,1,0], [0,0,0,1], [0,-Fe/mt,-mu/mt, 0], [0,0,0,0]])
Blat = np.matrix([[0],[0],[0],[1.0/(Jc + 2*mp*d**2)]])
Clat = np.matrix([[1,0,0,0], [0,1,0,0]])

#  tuning parameters
tr_h =  0.2
tr_th = 0.08
tr_z = tr_th * 5
zeta = 0.707

# gain calculation
wn_h  = 2.2/tr_h
wn_th = 2.2/tr_th  # natural frequency
wn_z  = 2.2/tr_z
des_char_poly_lon = [1, 2*zeta*wn_h, wn_h**2]
des_poles_lon = np.roots(des_char_poly_lon)

des_char_poly_lat = np.convolve([1, 2*zeta*wn_z, wn_z**2], [1, 2*zeta*wn_th, wn_th**2])
des_poles_lat = np.roots(des_char_poly_lat)

print "poles lon:",des_poles_lon
print "poles lat:",des_poles_lat

# Compute the gains if the system is controllable
if np.linalg.matrix_rank(cnt.ctrb(Alon, Blon)) != 2 \
    or np.linalg.matrix_rank(cnt.ctrb(Alat, Blat)) != 4:
    print("The system is not controllable")
else:
    K_lon = cnt.acker(Alon, Blon, des_poles_lon)
    kr_lon = -1.0/(Clon[0]*np.linalg.inv(Alon-Blon*K_lon)*Blon)

    K_lat = cnt.acker(Alat, Blat, des_poles_lat)
    kr_lat = -1.0/(Clat[0]*np.linalg.inv(Alat-Blat*K_lat)*Blat)

    print('K_lon: ', K_lon)
    print('kr_lon: ', kr_lon)
    print('K_lat: ', K_lat)
    print('kr_lat: ', kr_lat)
