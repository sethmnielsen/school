import numpy as np
from math import log10, floor
from scipy import linalg as la

np.set_printoptions(suppress=True)

def round_sig(x, sig=3):
    if x.size == 1 and x==0:
        return x
    elif type(x) != np.ndarray:
        x = round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        for i in range(x.size):
            x[i] = round(x[i], sig-int(floor(log10(abs(x[i]))))-1)

    return x

def solve_lu(A, b):
    c = b
    m = A.shape[0]
    x = np.zeros(m)
    y = np.zeros(m)
    E = np.array([np.eye(m)]*(m-1))
    E_inv = np.copy(E)
    U = np.copy(A)
    L = np.eye(m)

    # LU decomposition
    for j in range(m-1): # loop through cols of A
        vals = - round_sig(U[j+1:m,j] / U[j,j])
        E[j,j+1:m,j] = vals
        E_inv[j,j+1:m,j] = -vals

        U = E[j] @ U
        L = L @ E_inv[j]

    print('U=',U)
    print('L=',L)

    # Forward substitution
    for j in range(m):
        y[j] = round_sig(c[j] - L[j,:][:j] @ y[:j])

    # Back substitution
    for j in range(m-1,-1,-1):
        x[j] = ( 1/U[j,j] )*( y[j] - U[j,:][j+1:] @ x[j+1:] )

    return x

def solve_lu_pivot(A, b):
    P, L, U = la.lu(A)

    c = P.T@b
    m = A.shape[0]
    x = np.zeros(m)
    y = np.zeros(m)

    print('U=',U)
    print('L=',L)

    # Forward substitution
    for j in range(m):
        y[j] = round_sig(c[j] - L[j,:][:j] @ y[:j])

    # Back substitution
    for j in range(m-1,-1,-1):
        x[j] = ( 1/U[j,j] )*( y[j] - U[j,:][j+1:] @ x[j+1:] )

    return x

A = np.array([[2,4,-5],
              [6,12.001,1],
              [4,-8,-3]])

b = np.array([-5,33.002,-21])

x = solve_lu(A,b)
x_pivot = solve_lu_pivot(A,b)

print('x=',x)
print('x_pivot=',x_pivot)
