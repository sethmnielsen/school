import numpy as np
np.set_printoptions(precision=3)

m = 5     # number of parameters
n = 1000  # iterations

h = np.array([1,2,3,4,5])  # impulse response
hhat = np.zeros(m)         # initial estimated parameters
f = np.random.randn(n)     # normally-distributed random input
fn = np.hstack(([0,0,0,0],f))  # convenience array used to shift through input (f)
q = np.zeros(m)  # input data for one time step
delta = .0001
P = 1/delta * np.eye(m)  # initial P

for i in range(n):
    d = fn[i:i+5] @ h  # true output
    q = fn[i:i+m]      # q update

    k = P @ q / (1 + q.T @ P @ q)  # kalman gain vector
    y = q @ hhat  # filter output
    e = d - y     # error

    hhat = hhat + k * e  # update of estimated parameters
    P = P - k * q @ P    # P update

print('hhat:',hhat)
