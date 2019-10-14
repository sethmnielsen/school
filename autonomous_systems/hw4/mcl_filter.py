#!usr/env python3

import numpy as np
import scipy as sp

from params import *
from utils import wrap

class MCL():
    def __init__(self):
        self.xhat = np.array([x0, y0, th0])
        self.Sigma = np.eye(3)
        
        self.dt = dt
        kappa = 4.0
        alpha = 0.4
        beta = 2
        self.n = 7 # augmented state dimension
        self.lamb = alpha**2 * (self.n + kappa) - self.n

        # weights
        self.wm = np.zeros(2 * self.n + 1)
        self.wc = np.zeros_like(self.wm)

        self.wm[0] = self.lamb / (self.n + self.lamb)
        self.wc[0] = self.wm[0] + (1 - alpha**2 + beta)

        self.wm[1:] = 1.0 / (2 * (self.n + self.lamb))
        self.wc[1:] = 1.0 / (2 * (self.n + self.lamb))