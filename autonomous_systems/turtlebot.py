#!/usr/env python3

import numpy as np

from params import *
from utils import wrap

class Turtlebot():
    def __init__(self):
        self.state = np.array([x0, y0, th0]) # x, y, theta

        # time
        self.dt = dt
        self.t_end = 20
        self.t = np.arange(0, self.t_end, self.dt)
        self.N = len(self.t)

        # velocities
        self.v = np.zeros(self.N)
        self.omg = np.zeros(self.N)
        self.vc = np.zeros(self.N)
        self.omgc = np.zeros(self.N)

    def build_vel_arrays(self):
        alphas = vm_alphas
        
        # v/omg commands
        self.vc = 1 + .5 * np.cos(2 * np.pi * 0.3 * self.t) # 0.2 on HW3 pdf
        self.omgc = -0.2 + 2 * np.cos(2 * np.pi * 1.0 * self.t) # 0.6 on HW3 pdf
        
        # v/omg real outputs (noise added)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            dddddddddddddddddddddddd
        v_noise_arr = np.random.randn(self.N)
        omg_noise_arr = np.random.randn(self.N)
        sample_v = alphas[0] * self.vc**2 + alphas[1] * self.omgc**2
        sample_omg = alphas[2] * self.vc**2 + alphas[3] * self.omgc**2
        
        self.v = self.vc + np.sqrt(sample_v) * v_noise_arr
        self.omg = self.omgc + np.sqrt(sample_omg) * omg_noise_arr

    def propagate_truth(self, i):
        # calculate x, y, th
        x, y, th = self.state
        vo = self.v[i]/self.omg[i]
        th_plus = wrap(th + self.omg[i]*self.dt)

        x = x - vo*np.sin(th) + vo*np.sin(th_plus)
        y = y + vo*np.cos(th) - vo*np.cos(th_plus)
        th = th_plus
        self.state = np.array([x, y, th])

    def get_measurements(self) -> np.ndarray:
        x, y, th = self.state
        mdx = lmarks[0] - x
        mdy = lmarks[1] - y
        
        # senor noise
        r_noise = np.random.normal(0, sigs[0], num_lms)
        phi_noise = np.random.normal(0, sigs[1], num_lms)
        
        # compute simulated r and phi measurements
        r = np.sqrt(np.add(mdx**2,mdy**2)) + r_noise
        phi_raw = wrap(np.arctan2(mdy, mdx) - th)
        phi = wrap(np.array(phi_raw)) + phi_noise

        self.zt = np.vstack((r, phi))
        return self.zt