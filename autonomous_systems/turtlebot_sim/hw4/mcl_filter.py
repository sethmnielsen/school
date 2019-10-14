#!usr/env python3

import numpy as np
import scipy as sp

import params as pm
from utils import wrap

class MCL():
    def __init__(self):
        self.xhat = np.array(state0)

        self.Chi = np.zeros((3, pm.M))
        self.Chi[2].fill(1/pm.M)
        self.Chi[:2] = np.random.rand(2, pm.M) * 20

    def update(self, v, omg, z):
        for i in range(pm.M):
            state = self.xhat
            

    # def 