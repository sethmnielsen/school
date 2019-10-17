#!usr/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# from turtlebot import Turtlebot
import sys
sys.path.append("..")
from turtlebot import Turtlebot
import params as pm
from utils import wrap

class MCL():
    def __init__(self, tbot:Turtlebot):
        self.Chi = np.zeros((3,pm.M))
        self.Chi[:2] = np.random.rand(2, pm.M) * 20 - 10
        self.Chi[2] = np.random.rand(pm.M) * 2*np.pi - np.pi
        
        # plt.plot(self.Chi[0], self.Chi[1], '.', color='orange')
        # plt.show()
        
        m = pm.M
        self.w = np.zeros(pm.M)
        self.w.fill(1/pm.M)

        self.tbot = tbot

    def update(self, v, omg, z):
        w_lmarks = np.ones((pm.num_lms,pm.M))
        self.Chi = self.tbot.sample_motion_model(v, omg, self.Chi, particles=True)
        for i in range(pm.M):
            zhat = self.tbot.get_measurements(self.Chi[:,i], particles=True)
            zdiff = z - zhat
            zdiff = wrap( z - zhat, dim=1 )
            for k in range(pm.num_lms):
                w_lmarks[k,i] *= self.measurement_prob(zdiff[:,k], 2*pm.sigs)
        #     self.Chi[:,i] = self.tbot.sample_motion_model(v, omg, self.Chi[:,i])
        #     zhat = self.tbot.get_measurements(self.Chi[:,i], particle=True)
        #     zdiff = z - zhat
        #     zdiff = wrap( z - zhat, dim=1 )
        #     for k in range(pm.num_lms):
        #         w_lmarks[k,i] *= self.measurement_prob(zdiff[:,k], 2*pm.sigs)

        # w_lmarks = w_lmarks/np.sum(w_lmarks, axis=1)[:,np.newaxis]
        self.w = np.prod( w_lmarks, axis=0 )
        self.w = self.w / np.sum(self.w)
        if not np.all(np.isfinite(self.w)):
            print( 'WE GOT A NAN !')
        self.Chi = self.low_variance_sampler()
        return self.Chi

    def measurement_prob(self, zdiff, sigs):
        # zdiff.shape = (2,3), sigs.shape = (2,)
        temp1 = 1/np.sqrt(2*np.pi*sigs**2)
        temp2 = np.exp( -zdiff**2 / (2*sigs**2) )
        prob = temp1*temp2
        return np.prod( prob, axis=0 )
    
    def low_variance_sampler(self):
        r = np.random.rand() * 1/pm.M
        c = self.w[0]
        i = 1
        inds = []
        for m in range(1, pm.M+1):
            U = r + (m - 1) * 1/pm.M
            while U > c:
                i += 1
                c += self.w[i-1]
            inds.append(i-1)

        return self.Chi[:, inds]