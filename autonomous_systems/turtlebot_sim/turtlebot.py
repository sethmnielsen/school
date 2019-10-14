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
        self.states[:, 0] = np.copy(pm.state0)

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

    # Accepts either number or array of numbers for v, omg, state
    def sample_motion_model(self, v, omg, state):
        alphas = pm.alphas

        alpha_v = alphas[0]*v**2 + alphas[2]*omg
        alpha_omg = alphas[2]*v**2 + alphas[3]*omg

        if isinstance(v, np.ndarray):
            noise_v = np.random.randn( v.shape[0] )
            noise_omg = np.random.randn( v.shape[0] )
        else:
            noise_v = np.random.randn()
            noise_omg = np.random.randn()

        sample_v = np.sqrt(alpha_v) * noise_v
        sample_omg = np.sqrt(alpha_omg) * noise_omg

        vhat = v + sample_v
        omghat = omg + sample_omg

        return self.propagate_state(vhat, omghat, state)
       
    def propagate_state(self, v, omg, state):
        # calculate x, y, th
        x, y, th = state
        vo = v/omg
        th_plus = wrap(th + omg*pm.dt)

        x = x - vo*np.sin(th) + vo*np.sin(th_plus)
        y = y + vo*np.cos(th) - vo*np.cos(th_plus)
        th = th_plus
        state = np.array([x, y, th])
        return state

    def get_measurements(self, state: np.ndarray) -> np.ndarray:
        x, y, th = state
        mdx = pm.lmarks[0] - x
        mdy = pm.lmarks[1] - y
        
        # senor noise
        r_noise = np.random.normal(0, pm.sigs[0], pm.num_lms)
        phi_noise = np.random.normal(0, pm.sigs[1], pm.num_lms)
        
        # compute simulated r and phi measurements
        r = np.sqrt(np.add(mdx**2,mdy**2)) + r_noise
        phi_raw = wrap(np.arctan2(mdy, mdx) - th)
        phi = wrap(np.array(phi_raw)) + phi_noise

        z = np.vstack((r, phi))
        return z