import numpy as np

m = 5  # number of parameters
n = 10  # iterations

h = np.array([1,2,3,4,5])  # impulse response
hh = np.zeros(m)  # hhat - estimated parameters
f = np.random.randn(n)
fn = np.hstack(([0,0,0,0],f))  # fnew
delta = .0001
P = 1/delta * np.eye(m)
q = np.zeros(m)

# q = u
# h = c
# hh = chat
# e = d - q.H * h is like e = y - yhat

for i in range(n):
    d = fn[i:i+5] @ h  # fn update
    print(d)
    q = np.hstack((f[i],q[:-1]))  # q update

    k = P @ q / (1 + q.T @ P @ q)
    e = d - q @ hh

    hh = hh + k * e
    P = P - k * q @ P

print('hh=\n',hh)
