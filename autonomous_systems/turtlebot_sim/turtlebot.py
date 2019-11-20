#!/usr/env python3
import shared

if shared.USE_CUPY:
    import cupy as xp
else:
    import numpy as xp

from utils import wrap

class Turtlebot():
    def __init__(self, params, particles=False, vc=None, omgc=None):
        self.pm = params
        
        # time
        self.N = len(self.pm.t_arr)

        # Current state, state history array
        self.states = xp.zeros((3, self.N))
        self.states[:,0] = self.pm.state0

        # velocities
        if vc is not None and omgc is not None:
            build_vel_arrays = False
            self.vc = vc
            self.omgc = omgc
        else:
            build_vel_arrays = True
            self.vc = xp.zeros(self.N)
            self.omgc = xp.zeros(self.N)

        self.v = xp.zeros(self.N)
        self.omg = xp.zeros(self.N)

        if build_vel_arrays:
            self.build_vel_and_state(particles)
        else:
            self.states = self.sample_motion_model(self.vc, self.omgc, self.states, particles)

    def build_vel_and_state(self, particles=False):
        alphas = self.pm.alphas
        
        # v/omg commands
        self.vc = 1 + .5 * xp.cos(2 * xp.pi * 0.2 * self.pm.t_arr) # 0.2 on HW3 pdf
        self.omgc = -0.2 + 2 * xp.cos(2 * xp.pi * 0.6 * self.pm.t_arr) # 0.6 on HW3 pdf
        
        # v/omg real outputs (noise added)
        self.states = self.sample_motion_model(self.vc, self.omgc, self.states, particles)

    def sample_motion_model(self, vc, omgc, state, particles=False):
        # Accepts either number or array of numbers for vc, omgc, state
        alphas = self.pm.alphas

        sd_v   = xp.sqrt( alphas[0]*(vc**2) + alphas[1]*(omgc**2) )
        sd_omg = xp.sqrt( alphas[2]*(vc**2) + alphas[3]*(omgc**2) )

        if particles:
            m = 10  # noise multiplier
            n = self.pm.M  # number of random numbers to generate
            propagate = self.propagate_particles

            sd_gam = xp.sqrt( alphas[4]*(vc**2) + alphas[5]*(omgc**2) )
            noise_gam = xp.random.randn( n )

        else:
            m = 1  # noise multiplier
            n = vc.shape[0]  # number of random numbers to generate
            propagate = self.propagate_state

            sd_gam = xp.zeros(self.v.shape)
            noise_gam = 0

        self.v = vc + sd_v*xp.random.randn( n ) * m
        self.omg = omgc + sd_omg*xp.random.randn( n ) * m
        gam = sd_gam*noise_gam * m
        
        return propagate(state, self.v, self.omg, gam)
       
    def propagate_state(self, state, v, omg, gam):
        n = v.shape[0]
        for k in range(n-1):
            state[:,k+1] = self.compute_next_state(xp.array(state[:,k]), v[k+1], omg[k+1], gam[k+1])

        state = wrap(state,2)
        return state

    def propagate_particles(self, Chi, vhat, omghat, gamhat=0):
        Chi = self.compute_next_particles(Chi, vhat, omghat, gamhat)
        return Chi

    def compute_next_particles(self, Chi, vhat, omghat, gamhat):
        Chi = self.compute_next_state(Chi, vhat, omghat, gamhat)
        mask = abs(Chi[2]) > xp.pi
        Chi[2][mask] = wrap(Chi[2][mask])
        return Chi

    def compute_next_state(self, x, v, omg, gam):
        vo = v/omg
        th = x[2]
        th_plus = th + omg*self.pm.dt
        
        x += xp.hstack((-vo*xp.sin(th) + vo*xp.sin(th_plus),
                      vo*xp.cos(th) - vo*xp.cos(th_plus),
                      omg*self.pm.dt + gam*self.pm.dt))
        
        return x

    def get_measurements(self, state, particles=False) -> xp.ndarray:
        x, y, th = state
        mdx = self.pm.lmarks[0] - x
        mdy = self.pm.lmarks[1] - y

        # sensor noise
        if particles:
            r_noise = 0
            phi_noise = 0
        else:
            r_noise = xp.random.normal(0, self.pm.sig_r, self.pm.num_lms)
            phi_noise = xp.random.normal(0, self.pm.sig_phi, self.pm.num_lms)

        # compute simulated r and phi measurements
        r = xp.sqrt(xp.add(mdx**2,mdy**2))
        phi = xp.arctan2(mdy, mdx) - th
        phi = wrap(phi)

        # Check for landmarks within range of sensor
        r += r_noise
        detected_mask = (abs(phi) <= self.pm.fov/2) & (r <= self.pm.rho)
        phi += phi_noise
        phi = wrap(phi)
        
        z = xp.vstack((r, phi))
        return z, detected_mask

