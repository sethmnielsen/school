import numpy as np
import scipy.linalg as spl

A = np.array([[10000, 10001, 10002, 10003, 10004], [10001, 10002, 10003, 10004, 10005]]).T
b = np.array([20001, 20003, 20005, 20007, 20009])

x = np.linalg.inv(A.T @ A) @ A.T @ b

Q, R = spl.qr(A)

y_qr = np.linalg.solve(Q, b.reshape(5,1))
x_qr = np.linalg.solve(R[:2], y_qr[:2])

print('x_qr=\n', x_qr)


L = np.linalg.cholesky(A.T @ A)

y_ch = np.linalg.solve(L, A.T @ b.reshape(5,1))
x_ch = np.linalg.solve(L.T, y_ch)

print('x_ch=\n', x_ch)
