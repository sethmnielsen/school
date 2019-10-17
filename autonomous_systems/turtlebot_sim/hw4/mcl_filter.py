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
        self.tbot = tbot

        self.Chi = np.zeros((3,pm.M))
        self.Chi[:2] = np.random.rand(2, pm.M) * 20 - 10
        self.Chi[2] = np.random.rand(pm.M) * 2*np.pi - np.pi
        
        self.xhat = np.mean(self.Chi, axis=1, keepdims=True)
        x_error = wrap(self.Chi - self.xhat, dim=2)
        self.sigma = np.cov(x_error)

        # plt.plot(self.Chi[0], self.Chi[1], '.', color='orange')
        # plt.show()
        
        m = pm.M
        self.w = np.zeros(pm.M)
        self.w.fill(1/pm.M)

    def update(self, v, omg, z):
        w_lmarks = np.ones((pm.num_lms,pm.M))
        self.Chi = self.tbot.sample_motion_model(v, omg, self.Chi, particles=True)
        for i in range(pm.M):
            zhat = self.tbot.get_measurements(self.Chi[:,i], particles=True)
            zdiff = z - zhat
            zdiff = wrap( z - zhat, dim=1 )
            for k in range(pm.num_lms):
                w_lmarks[k,i] *= self.measurement_prob(zdiff[:,k], 2*pm.sigs)

        w_lmarks = w_lmarks/np.sum(w_lmarks, axis=1)[:,np.newaxis]
        self.w = np.prod( w_lmarks, axis=0 )
        self.w = self.w / np.sum(self.w)
        if not np.all(np.isfinite(self.w)):
            print( 'WE GOT A NAN !')
        self.Chi = self.low_variance_sampler()

        self.xhat = wrap( np.mean(self.Chi, axis=1, keepdims=True), 2)
        x_error = wrap( self.Chi - self.xhat, 2)
        self.sigma = np.cov(x_error)


    def measurement_prob(self, zdiff, sigs):
        # zdiff.shape = (2,3), sigs.shape = (2,)
        temp1 = 1/np.sqrt(2*np.pi*sigs**2)
        temp2 = np.exp( -zdiff**2 / (2*sigs**2) )
        prob = temp1*temp2
        return np.prod( prob, axis=0 )
    
    def low_variance_sampler(self):
        M_inv = 1/pm.M
        r = np.random.uniform(0, M_inv)
        c = np.cumsum(self.w)
        U = np.arange(pm.M)*M_inv + r
        diff = c- U[:,None]
        i = np.argmax(diff > 0, axis=1)

        return self.Chi[:,i]