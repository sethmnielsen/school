#!/usr/env python3

import numpy as np
from utils import wrap
import hw6.params as pm

class Turtlebot():
    def __init__(self, params, vc=None, omgc=None):
        # time
        self.N = len(pm.t_arr)

        # Current state, state history array
        self.states = np.zeros((3, self.N))
        self.states[:,0] = pm.state0
        build_vel_arrays = True

        # velocities
        if vc is not None and omgc is not None:
            self.vc = vc
            self.omgc = omgc
            build_vel_arrays = False
        else:
            self.vc = np.zeros(self.N)
            self.omgc = np.zeros(self.N)

        self.v = np.zeros(self.N)
        self.omg = np.zeros(self.N)

        if build_vel_arrays:
            self.build_vel_and_state()
        else:
            self.sample_motion_model(self.vc, self.omgc, self.states)

    def build_vel_and_state(self):
        alphas = pm.alphas
        
        # v/omg commands
        self.vc = 1 + .5 * np.cos(2 * np.pi * 0.2 * pm.t_arr) # 0.2 on HW3 pdf
        self.omgc = -0.2 + 2 * np.cos(2 * np.pi * 0.6 * pm.t_arr) # 0.6 on HW3 pdf
        
        # v/omg real outputs (noise added)
        self.states = self.sample_motion_model(self.vc, self.omgc, self.states)

    def sample_motion_model(self, vc, omgc, state, particles=False):
        # Accepts either number or array of numbers for vc, omgc, state
        alphas = pm.alphas

        sd_v   = np.sqrt( alphas[0]*(vc**2) + alphas[1]*(omgc**2) )
        sd_omg = np.sqrt( alphas[2]*(vc**2) + alphas[3]*(omgc**2) )

        if particles:
            m = 10  # noise multiplier
            n = pm.M  # number of random numbers to generate
            propagate = self.propagate_particles

            sd_gam = np.sqrt( alphas[4]*(vc**2) + alphas[5]*(omgc**2) )
            noise_gam = np.random.randn( n )

        else:
            m = 1  # noise multiplier
            n = vc.shape[0]  # number of random numbers to generate
            propagate = self.propagate_state

            sd_gam = np.zeros(self.v.shape)
            noise_gam = 0

        self.v = vc + sd_v*np.random.randn( n ) * m
        self.omg = omgc + sd_omg*np.random.randn( n ) * m
        gam = sd_gam*noise_gam * m
        
        return propagate(state, self.v, self.omg, gam)
       
    def propagate_state(self, state, v, omg, gam):
        n = v.shape[0]
        for k in range(n-1):
            state[:,k+1] = self.compute_next_state(state[:,k], v[k+1], omg[k+1], gam[k+1])

        return wrap(state, 2)

    def propagate_particles(self, Chi, vhat, omghat, gamhat=0):
        Chi = self.compute_next_particles(Chi, vhat, omghat, gamhat)
        return Chi

    def compute_next_particles(self, Chi, vhat, omghat, gamhat):
        Chi = self.compute_next_state(Chi, vhat, omghat, gamhat)
        mask = abs(Chi[2]) > np.pi
        Chi[2][mask] = wrap(Chi[2][mask])
        return Chi

    def compute_next_state(self, x, v, omg, gam):
        vo = v/omg
        th = x[2]
        th_plus = th + omg*pm.dt
        
        x += np.array([-vo*np.sin(th) + vo*np.sin(th_plus),
                      vo*np.cos(th) - vo*np.cos(th_plus),
                      omg*pm.dt + gam*pm.dt])
        
        return x

    def get_measurements(self, state, lmark=pm.lmarks, particles=False) -> np.ndarray:
        x, y, th = state
        mdx = lmark[0] - x
        mdy = lmark[1] - y

        # senor noise
        if particles:
            r_noise = 0
            phi_noise = 0
        else:
            r_noise = np.random.normal(0, pm.sig_r, pm.num_lms)
            phi_noise = np.random.normal(0, pm.sig_phi, pm.num_lms)

        # compute simulated r and phi measurements
        r = np.sqrt(np.add(mdx**2,mdy**2)) + r_noise
        phi_raw = np.arctan2(mdy, mdx) - th + phi_noise
        phi = wrap(phi_raw)

        z = np.vstack((r, phi))  # returns (2,3) array, combo of (r, phi) for each lmark
        return z