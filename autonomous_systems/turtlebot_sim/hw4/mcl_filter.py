#!usr/env python3

import numpy as np
import scipy as sp

import params as pm
from utils import wrap

class MCL():
    def __init__(self):
        self.Chi = np.zeros(np.M)
        


    def update(self, v, omg, z):
        Chi = []
        for i in range(pm.M):
            x = 0


    # def 