import numpy as np

def solve_lu(L, U, b):
    c = b
    m = c.size
    x = np.zeros(m)
    y = np.zeros(m)

    # Forward substitution
    for j in range(m):
        y[j] = c[j] - L[j,:][:j] @ y[:j]

    # Back substitution
    for j in range(m-1,-1,-1):
        x[j] = ( 1/U[j][j] )*( y[j] - U[j,:][j+1:] @ x[j+1:] )

    return x


L = np.array([[1,0],[2,1]])
U = np.array([[3,4],
              [0,5]])
b = np.array([6,7])

x = solve_lu(L,U,b)

print(x)
