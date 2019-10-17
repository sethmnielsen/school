#!usr/env python3

import numpy as np
import scipy as sp

# from turtlebot import Turtlebot
import sys
sys.path.append("..")
from turtlebot import Turtlebot
import params as pm
from utils import wrap

class MCL():
    def __init__(self, tbot:Turtlebot):
        self.Chi = np.zeros((3,pm.M))
        self.Chi[:2] = np.random.rand(2, pm.M) * 20
        self.Chi[2] = np.random.rand(pm.M) * 2*np.pi - np.pi

        m = pm.M
        self.w = np.zeros(pm.M)
        self.w.fill(1/pm.M)

        self.tbot = tbot

    def update(self, v, omg, z):
        w_lmarks = np.ones((pm.num_lms,pm.M))
        for i in range(pm.M):
            self.Chi[i] = self.tbot.sample_motion_model(v, omg, self.Chi[:,i])
            zhat = self.tbot.get_measurements(self.Chi[:,i])
            w_lmarks[:,i] = self.measurement_prob(z - zhat, pm.sigs)
        self.w = w_lmarks/np.sum(w_lmarks, axis=1)[:,np.newaxis]
        if not np.all(np.isfinite(self.w)):
            print( 'WE GOT A NAN !')
        self.Chi = self.low_variance_sampler()
        return self.Chi

    def measurement_prob(self, zdiff, sigs):
        # zdiff.shape = (2,3), sigs.shape = (2,)
        temp1 = 1/np.sqrt(2*np.pi*sigs.reshape(2,1)**2)
        temp2 = np.exp( -zdiff**2 / (2*sigs.reshape(2,1)**2) )
        prob = temp1*temp2
        return np.prod(np.prod(prob), axis=0)
    
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
            Chi_bar.append( self.Chi[i] )
        
        return np.array(Chi_bar)