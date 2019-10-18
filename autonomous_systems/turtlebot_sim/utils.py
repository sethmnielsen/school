import numpy as np
import timeit

def wrap(angle, dim=None):
    if isinstance(angle, np.ndarray) and angle.size == 0:
         return angle

    if dim:
        angle[dim] -= 2*np.pi * np.floor((angle[dim] + np.pi) / (2*np.pi))
    else:
        angle -= 2*np.pi * np.floor((angle + np.pi) / (2*np.pi))
    return angle