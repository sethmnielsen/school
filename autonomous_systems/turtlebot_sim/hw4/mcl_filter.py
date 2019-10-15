#!usr/env python3

import numpy as np
import scipy as sp

# from turtlebot import Turtlebot
import turtlebot.Turtlebot as tbot
import params as pm
from utils import wrap

class MCL():
    def __init__(self):
        self.Chi = np.zeros((pm.M, 3))
        self.Chi[:, :2] = np.random.rand(2, pm.M) * 20
        self.Chi[:, 2] = np.random.rand(pm.M) * 2*np.pi - np.pi

        self.w = np.zeros(pm.M)
        self.w = self.w.fill(1/pm.M)

    def update(self, v, omg, z):
        for i in range(pm.M):
            self.Chi[i] = tbot.sample_motion_model(v, omg, self.Chi[i])
            zhat = tbot.get_measurements(self.Chi[i])
            self.w[i] = self.measurement_prob(z - zhat, pm.sigs)
        self.Chi = self.low_variance_sampler()
        return self.Chi

    def measurement_prob(self, zdiff, sigs):
        temp1 = 1/np.sqrt(2*np.pi*sigs**2)
        temp2 = np.exp( -zdiff**2 / (2*sigs**2) )
        prob = temp1*temp2
        return prob[0] @ prob[1]
    
    def low_variance_sampler(self):
        Chi_bar = []
        r = np.random.rand() * 1/pm.M
        c = self.w[0]
        i = 0
        for m in range(pm.M):
            U = r + (m - 1) * 1/pm.M
            while U > c:
                i += 1
                c = c + self.w[i]
            Chi_bar.append(self.Chi[i])
        
        return np.array(Chi_bar)