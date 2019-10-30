#!/usr/env python3

import numpy as np
from utils import wrap

pm = None

class Turtlebot():
    def __init__(self, params):
        pm = params
        # time
        self.t_end = pm.t_end
        self.N = len(pm.t_arr)

        # Current state, state history array
        self.states = np.zeros((3, self.N))
        self.states[:,0] = pm.state0

        # velocities
        self.vc = np.zeros(self.N)
        self.omgc = np.zeros(self.N)


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
        sd_gam = np.sqrt( alphas[4]*(vc**2) + alphas[5]*(omgc**2) )

        # if isinstance(vc, np.ndarray):
        if particles:
            m = 10  # noise multiplier
            n = pm.M  # number of random numbers to generate
            noise_gam = np.random.randn( n )
            propagate = self.propagate_particles
        else:
            m = 1  # noise multiplier
            n = vc.shape[0]  # number of random numbers to generate
            noise_gam = 0
            propagate = self.propagate_state

        vhat = vc + sd_v*np.random.randn( n ) * m
        omghat = omgc + sd_omg*np.random.randn( n ) * m
        gamhat = sd_gam*noise_gam * m
        
        return propagate(state, vhat, omghat, gamhat)
       
    def propagate_state(self, state, v, omg, gam=0):
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

    def get_measurements(self, state, lmark=pm.lmarks, particles=True) -> np.ndarray:
        x, y, th = state
        mdx = lmark[0] - x
        mdy = lmark[1] - y

        # senor noise
        if particles:
            r_noise = 0
            phi_noise = 0
        else:
            r_noise = np.random.normal(0, pm.sigs[0], pm.num_lms)
            phi_noise = np.random.normal(0, pm.sigs[1], pm.num_lms)

        # r_noise2 = pm.sig_r*np.random.randn(3)
        # phi_noise2 = pm.sig_phi*np.random.randn(3)

        # r_noise = r_noise2
        # phi_noise = phi_noise2
        # compute simulated r and phi measurements
        r = np.sqrt(np.add(mdx**2,mdy**2)) + r_noise
        phi_raw = np.arctan2(mdy, mdx) - th
        phi = wrap(phi_raw + phi_noise)

        z = np.vstack((r, phi))  # returns (2,3) array, combo of (r, phi) for each lmark
        return z





        # vo = v/omg
        # th = state[2]
        # th_plus = th + omg*pm.dt
        # s1 = np.sin(th)
        # s2 = np.sin(th_plus)
        # c1 = np.cos(th)
        # c2 = np.cos(th_plus)

        # A = np.array([-vo * s1 + vo * s2,
        #                 vo * c1 - vo * c2,
        #                 omg*pm.dt + gam*pm.dt])

        # state += A
        # angs_bad = state[2][ np.abs(state[2]) > np.pi ]
        # if angs_bad.shape[0] > 0:
        #     state = wrap(state, 2)