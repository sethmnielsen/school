## Batch Least Squares

import numpy as np
from numpy import linalg as npl

m = 3  # number of parameters
n = 10  # data points

c = [1.,2.,3.]  # real coefficients
c_h = np.zeros(m)  # c_hat - estimated parameters

Ts = 0.01
k = np.arange(n)
t = k*Ts

u = np.sin(0.01*t) + np.sin(0.1*t) + np.sin(t) + np.sin(10.*t)
A = np.zeros((n-2, 3))
A[:,0] = u[2:]
A[:,1] = u[1:-1]
A[:,2] = u[:-2]

d = A @ c

c_h = npl.inv(A.T @ A) @ A.T @ d

print('c_h =', c_h)

#### Plotting
# c_vec[:,0] = c[0]
# c_vec[:,1] = c[1]
# c_vec[:,2] = c[2]
#
# fig = plt.figure(dpi=150)
# plt.plot(t_vec, c_hvec[:,0], label='a1_hat')
# plt.plot(t_vec, c_hvec[:,1], label='a0_hat')
# plt.plot(t_vec, c_hvec[:,2], label='b0_hat')
#
# plt.plot(t_vec, c_vec[:,0], label='a1_real')
# plt.plot(t_vec, c_vec[:,1], label='a0_real')
# plt.plot(t_vec, c_vec[:,2], label='b0_real')
#
# plt.legend(loc='upper left')
# plt.xlabel('t')
# plt.ylabel('coefficient value')
# plt.show()
