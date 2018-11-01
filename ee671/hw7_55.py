import numpy as np

m = 3
n = 10000

h = np.array([1,2,3,4,5])
hh = np.zeros(m)
f = np.random.randn(n)
fn = np.hstack(([0,0,0,0],f))
delta = .0001
# d = np.zeros(n)
P = 1/delta * np.eye(m)
q = np.zeros(m)

for i in range(n):
    d = fn[i:i+5] @ h
    q = np.hstack((f[i],q[:-1]))

    k = P @ q / (1 + q.T @ P @ q)
    e = d - q @ hh

    hh = hh + k * e
    P = P - k * q @ P

print('hh=\n',hh)
