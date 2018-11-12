import numpy as np

N = 10
L = np.zeros((N-1,N-1))
a = np.zeros(N-1)
a[0] = -1
a[1] = 2
a[2] = -1

for i in range(N-1):
    L[i] = np.roll(a,i-1)

L[0,-1] = 0
L[-1,0] = 0

n = 1

lbda = 4*np.sin(n*np.pi/(2*N))**2
xn = np.sin(np.arange(1,N) * n*np.pi/N)

print('xn=\n',xn)
