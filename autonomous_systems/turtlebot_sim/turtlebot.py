#!/usr/env python3

import numpy as np

import params as pm
from utils import wrap

class Turtlebot():
    def __init__(self):
        # time
        self.t_end = 20
        self.N = len(pm.t_arr)

        # Current state, state history array
        self.states = np.zeros((3, self.N))
        self.states[:,0] = pm.state0

        # velocities
        self.vc = np.zeros(self.N)
        self.omgc = np.zeros(self.N)


    def build_vel_arrays(self):
        alphas = pm.alphas
        
        # v/omg commands
        self.vc = 1 + .5 * np.cos(2 * np.pi * 0.3 * pm.t_arr) # 0.2 on HW3 pdf
        self.omgc = -0.2 + 2 * np.cos(2 * np.pi * 1.0 * pm.t_arr) # 0.6 on HW3 pdf
        
        # v/omg real outputs (noise added)
        self.states = self.sample_motion_model(self.vc, self.omgc, self.states)

    def sample_motion_model(self, vc, omgc, state):
        # Accepts either number or array of numbers for vc, omgc, state
        alphas = pm.alphas

        sd_v = np.sqrt(alphas[0]*vc**2 + alphas[1]*omgc**2)
        sd_omg = np.sqrt(alphas[2]*vc**2 + alphas[3]*omgc**2)
        sd_gam = np.sqrt(alphas[4]*vc**2 + alphas[5]*omgc**2)

        if isinstance(vc, np.ndarray):
            noise_v = np.random.randn( vc.shape[0] )
            noise_omg = np.random.randn( vc.shape[0] )
            noise_gam = 0
        else:
            noise_v = np.random.randn()
            noise_omg = np.random.randn()
            noise_gam = np.random.randn()

        vhat = vc + sd_v*noise_v
        omghat = omgc + sd_omg*noise_omg
        gamhat = sd_gam*noise_gam

        return self.propagate_state(state, vhat, omghat, gamhat)
       
    def propagate_state(self, state, v, omg, gam):
        # Accepts either number or array of numbers for vhat, omghat, [gamhat], state
        # x, y, th = state
        # x, y, th = state[:,np.newaxis]
        # x, y, th = x.flatten(), y.flatten(), th.flatten()
        if isinstance(v, float):
            state = self.compute_curr_state(state, v, omg, gam)
        else:
            n = v.shape[0]
            for k in range(1,n):
                state[:,k] = self.compute_curr_state(state[:,k-1], v[k], omg[k])
        
        return state

    def compute_curr_state(self, state, v:float, omg:float, gam=0):
        x, y, th = state
        vo = v/omg
        
        th_plus = th + omg*pm.dt
        x = x - vo*np.sin(th) + vo*np.sin(th_plus)
        y = y + vo*np.cos(th) - vo*np.cos(th_plus)
        th = th_plus + gam*pm.dt

        return np.array([x, y, th])

    def get_measurements(self, state:np.ndarray, particle=True) -> np.ndarray:
        x, y, th = state
        mdx = pm.lmarks[0] - x
        mdy = pm.lmarks[1] - y

        # senor noise
        if particle:
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