## Recursive Least Squares

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

m = 3  # number of parameters
n = 1000  # iterations

c = [1.,2.,3.]  # real coefficients
c_h = np.zeros(m)  # c_hat - estimated parameters
t = 0
Ts = 0.01
delta = .000001
P = 1/delta * np.eye(m)
q = np.zeros(m)

t_vec = np.zeros(n)
c_hvec = np.zeros((n,m))
c_vec = np.zeros((n,m))

for k in range(n):
    t = k * Ts
    u = np.sin(0.01*t) + np.sin(0.1*t) + np.sin(t) + np.sin(10.*t)

    q = np.hstack( (u, q[:-1]) )   # q update, shift previous values over
    d = q @ c

    kal = P @ q / (1 + q.T @ P @ q)
    e = d - q @ c_h

    c_h = c_h + kal * e
    P = P - kal * q @ P

    t_vec[k] = t
    c_hvec[k] = c_h

print('c_h=\n',c_h)

#### Plotting
c_vec[:,0] = c[0]
c_vec[:,1] = c[1]
c_vec[:,2] = c[2]

fig = plt.figure(dpi=150)
plt.plot(t_vec, c_hvec[:,0], label='a1_hat')
plt.plot(t_vec, c_hvec[:,1], label='a0_hat')
plt.plot(t_vec, c_hvec[:,2], label='b0_hat')

plt.plot(t_vec, c_vec[:,0], label='a1_real')
plt.plot(t_vec, c_vec[:,1], label='a0_real')
plt.plot(t_vec, c_vec[:,2], label='b0_real')

plt.legend(loc='upper left')
plt.xlabel('t')
plt.ylabel('coefficient value')
plt.show()
