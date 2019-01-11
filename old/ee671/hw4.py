import numpy as np
from numpy import linalg as npl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

x = np.array([   2, 2.5, 3, 5,    9])
y = np.array([-4.2,  -5, 2, 1, 24.3])

#### Part b ####
A = np.column_stack([x, np.ones(5)])
## y = Ac + e
## c = (A.H * A)**-1 * A.H * y
c = npl.multi_dot([npl.inv(npl.multi_dot([A.conj().T, A])), A.conj().T, y])
y_ = np.dot(A, c)


#### Part c ####
W = np.diag(np.array([10, 1, 1, 1, 10]))  # weights
# c = (A.H * W * A)**-1 * A.H * W * y
c_w = npl.multi_dot([npl.inv(npl.multi_dot([A.conj().T, W, A])), A.conj().T, W, y])
y_w = np.dot(A, c_w)


#### Problem 12 part a ####

d = np.array([1, 1, 2, 3, 5, 8, 13])

A = np.array([[1, 1],
              [2, 1],
              [3, 2],
              [5, 3],
              [8, 5],
              [13, 8]])

R = A.T @ A

A_ac = np.vstack([[1, 0], A, [0, 13]])
R_ac = A_ac.T @ A_ac

#### Part b ####
## i
A_ = A[:-1]
a = npl.inv(A_.T @ A_) @ A_.T @ d[2:]

## ii
d_ac = np.hstack([ d[1:], [0,0] ])
a_ac = np.linalg.inv(A_ac.T @ A_ac) @ A_ac.T @ d_ac

print("Coefficients")
print("Covariance method:\n", a)
print("Autocorrelation method:\n", a_ac)

#### Part c ####
e = np.zeros(5)
for i in range(2, 6):
    e[i-2] = d[i] - (a[0]*d[i-1] + a[1]*d[i-2])

e_ac = np.zeros(len(d_ac))
for i in range(2, len(d_ac)):
    e_ac[i-2] = d_ac[i] - (a_ac[0]*d_ac[i-1] + a_ac[1]*d_ac[i-2])

e_norm = npl.norm(e)
e_ac_norm = npl.norm(e_ac)**2

print("\nMinimum least squares error")
print("Covariance method:\n", e_norm)
print("Autocorrelation method:\n", e_ac_norm)


#### Plotting

# fig = plt.figure(dpi=150)
# plt.scatter(x, y, label='raw data')
# plt.plot(x, y_, label='least-squares fit')
# plt.plot(x, y_w, label='least-squares weighted fit')
# plt.legend(loc='upper left')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()
