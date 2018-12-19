import matplotlib.pyplot as plt
import numpy as np
from msdDynamics import msdDynamics
import msdParam as param
import seaborn as sns
sns.set_style("white")
np.set_printoptions(precision=3)

msd = msdDynamics()

# Input signal (sine wave)
amplitude=5
frequency=0.1

m = 3     # number of parameters (k, b, m)
time = 50 # secs
n = int(time//param.Ts)  # iterations

hhat = np.zeros(m)         # initial estimated parameters

q = np.zeros(m)
delta = .00001
P = 1/delta * np.eye(m)  # initial P

d_arr = np.zeros(n)
y_arr = np.zeros(n)
t_arr = np.zeros(n)

t = param.t_start  # time starts at t_start
for i in range(n):
    u = [amplitude*np.sin(2*np.pi*frequency*t)]

    msd.propagateDynamics(u)
    d = msd.outputs()[0]
    q = np.hstack((u[0],q[:-1]))  # q update

    k = P @ q / (1 + q.T @ P @ q)  # kalman gain vector
    y = q @ hhat  # filter output
    e = d - y     # error

    hhat = hhat + k * e  # update of estimated parameters
    P = P - k * q @ P    # P update

    d_arr[i] = d
    y_arr[i] = y
    t_arr[i] = t

    t = t + param.Ts  # advance time by Ts

print('\nhhat:',hhat)

fig = plt.figure(dpi=150)
plt.plot(t_arr, d_arr, label='d')
plt.plot(t_arr, y_arr, label='y')
plt.xlabel('t')
plt.ylabel('output')
plt.legend(loc='upper left')

plt.show()
