import numpy as np
import numpy.linalg as la
import control
import sympy as sy
from sympy import Matrix

wn_th = 2.2
zeta_th = 0.707
a = 1
b = 2*zeta_th*wn_th
c = wn_th**2

p1_th, p2_th = np.roots([a, b, c])
print "theta poles =", p1_th, p2_th

wn_z = 0.22
zeta_z = 0.707
a = 1.0
b = 2.0*zeta_z*wn_z
c = wn_z**2.0

p1_z, p2_z = np.roots([a, b, c])
print "z poles =", p1_z, p2_z

m1 = 0.35
m2 = 2.0
l = 0.5
g = 9.81
ze = l/2.0
den = 1/(m1*ze**2 + m2*l**2 / 3.0)
A = np.matrix([[0,0,1,0],[0,0,0,1],[0,-9.81,0,0],[-m1*g/den,0,0,0]])
B = np.matrix([[0],[0],[0],[l/den]])
C = np.matrix([[1,0,0,0],[0,1,0,0]])

D1 = B
D2 = A*B
D3 = A**2 * B
D4 = A**3 * B
Cab = np.column_stack([D1, D2, D3, D4])
print "Cab ="
print Cab

if la.matrix_rank(Cab) == 4:
    print "Controllable"

# p = [p1_th,p2_th,p1_z,p2_z]
# p1 = [p1_th, p2_th, p1_z, -0.156]
# K = control.place(A, B, p1)
# print "K =", K

s = sy.symbols('s')
M = Matrix(s*np.identity(4) - A)
# print "det =", M.det()

a_A = np.array([0,0,0,-6.3506])
alpha = np.array([3.432,5.889,1.670,0.237])


K = (alpha - a_A) * la.inv(A) * la.inv(Cab)
print "K =", K

# Q = (A-B*K)
# eigs = la.eig(Q)
# print "eigs =", eigs
