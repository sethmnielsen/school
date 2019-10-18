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
        self.Chi[:2] = np.random.uniform(-10, 10, (2, pm.M))
        self.Chi[2] = np.random.uniform(-np.pi, np.pi, pm.M)
        
        self.xhat = np.mean(self.Chi, axis=1)
        x_errors = wrap(self.Chi - self.xhat[:,None], dim=2)
        self.sigma = np.cov(x_errors)

        m = pm.M
        self.w = np.zeros(pm.M)
        self.w.fill(1/pm.M)

    def update(self, v, omg, z):
        w_lmarks = np.ones((pm.num_lms,pm.M))
        self.Chi = self.tbot.sample_motion_model(v, omg, self.Chi, particles=True)
        for i in range(pm.num_lms):
            zhat = self.tbot.get_measurements(self.Chi, pm.lmarks[:,i], particles=True)
            zdiff = wrap( z[:,i,None] - zhat, dim=1 )
            w_lmarks[i] *= self.measurement_prob(zdiff, 2*pm.sigs)

        w_lmarks_normalized = w_lmarks/np.sum(w_lmarks, axis=1)[:,np.newaxis]
        if not np.all(np.isfinite(w_lmarks_normalized)):
            print( 'NAN RIGH HUR !')
        w_lmarks = w_lmarks_normalized
        self.w = np.prod( w_lmarks, axis=0 )
        self.w = self.w / np.sum(self.w)
        if not np.all(np.isfinite(self.w)):
            print( 'WE GOT A NAN !')
        self.Chi = self.low_variance_sampler()

        self.xhat = wrap( np.mean(self.Chi, axis=1), 2)
        x_errors = wrap( self.Chi - self.xhat[:,None], 2)
        self.sigma = np.cov(x_errors)


    def measurement_prob(self, zdiff, sigs):
        # zdiff.shape is (2,3), sigs.shape is (2,)
        temp1 = 1/np.sqrt(2*np.pi*sigs[:,None]**2)
        temp2 = np.exp( -zdiff**2 / (2*sigs[:,None]**2) )
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