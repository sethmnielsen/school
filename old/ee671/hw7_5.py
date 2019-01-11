import numpy as np

A = np.array([[4,6,4],[6,25,18],[4,18,22]])

L = np.linalg.cholesky(A)
m = L.shape[0]
U = np.eye(m)
D = np.eye(m)

for i in range(m):
    U[i+1:m,i] = L[i+1:m,i] / L[i,i]
    D[i,i] = L[i,i]**2

U = U.T

print('L=\n',L)
print('U=\n',U)
print('D=\n',D)
