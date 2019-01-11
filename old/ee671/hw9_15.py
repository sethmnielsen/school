import numpy as np
from numpy import linalg as npl
from scipy import linalg as spl
A = np.array([[ 4.84726, -2.46789, 0.549036, -4.31815 ],
              [ 0.813505, -3.46221, -0.251525, 2.97353]]).T
B = np.array([[ 4.51076, -2.18889, 0.58951, -4.715],
              [ 1.95213, -3.4499, -0.131083, 2.29282]]).T

U, S, Vh = spl.svd(B.T @ A)

Q = U @ Vh

print('Q =\n', Q)
print('Theta =', np.arccos(Q[0,0]))
