import numpy as np

m = 5  # number of parameters
n = 10000  # iterations

h = np.array([.5,-1,-2,1,.5])  # impulse response
hh = np.zeros(m)               # hhat - estimated parameters
sigma = np.sqrt(0.1)
f = np.random.randn(n) * sigma
fn = np.hstack(([0,0,0,0],f))  # fnew
mu = 3.5
q = np.zeros(m)

for i in range(n):
    d = fn[i:i+5] @ h  # fn update
    q = np.hstack((f[i],q[:-1]))  # q update
    e = d - q @ hh
    hh = hh + mu * q * e

print('hh=\n',hh)
