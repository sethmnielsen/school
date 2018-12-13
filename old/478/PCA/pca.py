import numpy as np
from numpy import linalg as la


x = [.2, -1.1, 1.0, .5, -.6]
y = [-.3, 2.0, -2.2, -1.0, 1.0]
m = 5

x_avg = 0
y_avg = -.1

xxcov = 0
xycov = 0
yycov = 0
for i in range(len(x)):
    xxcov += (x[i] - x_avg)**2
    xycov += (x[i] - x_avg) * (y[i] - y_avg)
    yycov += (y[i] - y_avg)**2

covar = np.matrix([[xxcov/m, xycov/m],
                   [xycov/m, yycov/m]])
w, v = la.eig(covar)
A = np.array([v[1,0], v[1,1]])
B = np.zeros((2,m))
print('A =',A)
B[0] = [i-x_avg for i in x]
B[1] = [i-y_avg for i in y]
print('B =',B)
T = np.dot(A,B)
print('T =',T)
