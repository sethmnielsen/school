import numpy as np
from scipy import linalg as spl

np.set_printoptions(precision=2, suppress=True, linewidth=150)

def myqr(A):
    n = A.shape[0]
    Q = np.eye(n)
    for k in range(n-1):
        Ak = (Q.T.conj() @ A)[k:,k:]
        x = Ak[:,0].reshape((n-k,1))
        alpha = -np.exp(1.0j*np.angle(x[0]))*spl.norm(x)
        e = np.zeros(((n-k),1))
        e[0] = 1.

        v = x + np.sign(x[0])*alpha * e
        v_ = np.zeros((n,1), dtype=np.complex128)
        v_[k:] = v

        Qk = np.eye(n, dtype=np.complex128) - 2* (v_ @ v_.T.conj())/ (v_.T.conj() @ v_)

        Q = Q @ Qk.T.conj()

    R = Q.T.conj() @ A

    return Q, R

n = 5   # size of square matrix
N = 10  # number of matrices to generate

A_real =      np.random.random((N,n,n))*200 - 100
A_imag = 1.0j*np.random.random((N,n,n))*200 - 100j
A = A_real + A_imag  # A is N complex matrices of size n x n

# Initialize as True; will be set False if the checks for any matrix fail
Q_unitary = True
R_upperTri = True
QR_equals_A = True
QR_same_result = True

# Call myqr function on all 10 matrices
for i in range(N):
    Q, R = myqr(A[i])
    Q_, R_ = spl.qr(A[i])

    # Checks
    if not np.allclose( Q @ Q.T.conj(), np.eye(n) ):  # check if Q is unitary
        Q_unitary = False

    if not np.allclose( R, np.triu(R) ):  # check if R is upper triangular
        R_upperTri = False

    if not np.allclose( Q @ R, A[i] ):  # check if QR = A
        QR_equals_A = False

    if not ( np.allclose(Q, Q_) and np.allclose(R, R_) ):
        QR_same_result = False

print('\nWas each Q unitary? {ans}'.format(ans='Yes' if Q_unitary else 'No'))
print('Was each R upper triangular? {ans}'.format(ans='Yes' if R_upperTri else 'No'))
print('Was QR = A true for each one? {ans}'.format(ans='Yes' if QR_equals_A else 'No'))
print('Did both functions give the same result each time? {ans}'.format(ans='Yes' if QR_same_result else 'No'))

print('\nPrinting last set of A, Q, and R matrices for display:\n')
print('A = \n', A[-1])
print('Q = \n', Q)
print('R = \n', R)

print('Q and R from SciPy qr function for comparision:\n')
print('Q = \n', Q_)
print('R = \n', R_)
