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
        self.states = np.zeros((self.N, 3))
        self.states[0] = pm.state0

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

        alpha_v = alphas[0]*vc**2 + alphas[1]*omgc**2
        alpha_omg = alphas[2]*vc**2 + alphas[3]*omgc**2

        if isinstance(vc, np.ndarray):
            noise_v = np.random.randn( vc.shape[0] )
            noise_omg = np.random.randn( vc.shape[0] )
        else:
            noise_v = np.random.randn()
            noise_omg = np.random.randn()

        sample_v = np.sqrt(alpha_v) * noise_v
        sample_omg = np.sqrt(alpha_omg) * noise_omg

        vhat = vc + sample_v
        omghat = omgc + sample_omg

        return self.propagate_state(vhat, omghat, state)
       
    def propagate_state(self, v, omg, state):
        # Accepts either number or array of numbers for vhat, omghat, state
        x, y, th = state.T
        vo = v/omg
        n = 1 if isinstance(v, float) else v.shape[0]
        
        for k in range(1,n):
            th_plus = th[k-1] + omg[k]*pm.dt
            x[k] = x[k-1] - vo[k]*np.sin(th[k-1]) + vo[k]*np.sin(th_plus)
            y[k] = y[k-1] + vo[k]*np.cos(th[k-1]) - vo[k]*np.cos(th_plus)
            th[k] = th_plus
        state = np.array([x, y, th]).T
        return state

    def get_measurements(self, state: np.ndarray) -> np.ndarray:
        x, y, th = state
        mdx = pm.lmarks[0] - x
        mdy = pm.lmarks[1] - y
        
        # senor noise
        r_noise = np.random.normal(0, pm.sigs[0], pm.num_lms)
        r_noise2 = np.sqrt((mdx-))
        phi_noise = np.random.normal(0, pm.sigs[1], pm.num_lms)
        
        # compute simulated r and phi measurements
        r = np.sqrt(np.add(mdx**2,mdy**2)) + r_noise
        phi_raw = np.arctan2(mdy, mdx) - th
        phi = wrap(phi_raw + phi_noise)

        z = np.vstack((r, phi))  # returns (2,3) array, combo of (r, phi) for each lmark
        return z