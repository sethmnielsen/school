import numpy as np
import numpy.linalg as npl

np.set_printoptions(precision=3, suppress=True)

M1 = np.array([[1, 1j,  0],
               [0,  1, 1j],
               [0, 1j, 0]])

M2 = np.array([[1+1j, 1+1j, 1+1j],
               [   2,   2,     2],
               [   0,   0,     0]])

M3 = np.array([[1-1j,  4,  5],
               [1-2j,  6,  7],
               [1-3j,  8,  9]])

u1 = M1 / npl.norm(M1, ord='fro')

y2 = M2 - np.trace(u1.T.conj() @ M2) * u1
u2 = y2 / npl.norm(y2, ord='fro')

y3 = M3 - np.trace(u2.T.conj() @ M3) * u2
u3 = y3 / npl.norm(y3, ord='fro')

N1 = u1
N2 = u2
N3 = u3

print("N1 =\n", N1)
print("\nN2 =\n", N2)
print("\nN3 =\n", N3)
