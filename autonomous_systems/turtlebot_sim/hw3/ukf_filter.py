#!usr/env python3

import numpy as np
import scipy as sp

import params as pm
from utils import wrap

class UKF():
    def __init__(self):
        self.xhat = np.array(pm.state0)
        self.Sigma = np.eye(3)
        
        kappa = 4.0
        alpha = 0.4
        beta = 2
        self.n = 7 # augmented state dimension
        self.lamb = alpha**2 * (self.n + kappa) - self.n
        self.Q = np.diag([pm.sig_r**2, pm.sig_phi**2])


        # weights
        self.wm = np.zeros(2 * self.n + 1)
        self.wc = np.zeros_like(self.wm)

        self.wm[0] = self.lamb / (self.n + self.lamb)
        self.wc[0] = self.wm[0] + (1 - alpha**2 + beta)

        self.wm[1:] = 1.0 / (2 * (self.n + self.lamb))
        self.wc[1:] = 1.0 / (2 * (self.n + self.lamb))
    
    def update(self, z: np.ndarray, v: float, omg: float):
        xhat, Sigma = np.copy(self.xhat), np.copy(self.Sigma)

        xhat_a, Sig_a = self.augment_state(xhat, Sigma, v, omg)

        # generate Sigma points
        L = sp.linalg.cholesky(Sig_a, lower=True)  
        Chi_a = self.generate_sigma_pts(xhat_a, L)

        # propagation - pass sig pts thru motion model and compute Gaussian statistics
        Chix_bar = self.propagate_sigma_pts(Chi_a[:3], Chi_a[3:5], v, omg)
        xbar = wrap(np.sum(self.wm * Chix_bar, axis=1), 2)

        diff_x = Chix_bar - xbar.reshape(3,1)
        diff_x = wrap(diff_x, 2)
        sum_ein_xx = np.einsum('ij, kj->jik', diff_x, diff_x)
        Sigma_bar = np.sum( self.wc.reshape(2*self.n + 1, 1, 1) * sum_ein_xx, axis=0)

        # it's measurement update time!
        for i in range(pm.num_lms):
            Zbar = self.gen_obs_sigmas(Chix_bar, Chi_a[5:], pm.lmarks[:,i])
            # mean of predicted meas
            zhat = np.sum(self.wm * Zbar, axis=1)  

            diff_z = Zbar - zhat.reshape(2,1)
            diff_z = wrap(diff_z, 1)
            sum_ein_zz = np.einsum('ij, kj->jik', diff_z, diff_z)
            sum_ein_xz = np.einsum('ij, kj->jik', diff_x, diff_z)
            # cov of predicted meas
            S = np.sum(self.wc.reshape(2 * self.n + 1, 1, 1) * sum_ein_zz, axis=0)  
            # cross cov btw state and observations (measurements)
            Sigma_xz = np.sum(self.wc.reshape(2 * self.n + 1, 1, 1) * sum_ein_xz, axis=0) 
        
            # Do that kalman gain 
            K = Sigma_xz @ np.linalg.inv(S)

            # update mean and covariance
            innov = z[:,i] - zhat
            innov = wrap(innov, 1)
            xhat = xbar + K @ (innov) # update location estimate - measurement update ****** make sure this doesn't do inner product but outer
            xhat = wrap(xhat, 2)  
            Sigma = Sigma_bar - K @ S @ K.T  # update location cov estimate

            # redraw sigma points (unless last landmark)
            if not i == (pm.num_lms - 1):
                xbar_a, Sigbar_a = self.augment_state(xbar, Sigma_bar, v, omg)
                L = sp.linalg.cholesky(Sigbar_a).T
                Chi_a = self.generate_sigma_pts(xbar_a, L)
                Chix_bar = Chi_a[:3]
                diff_x = Chix_bar - xbar.reshape(3,1)

        self.xhat, self.Sigma = xhat, Sigma

        return K

    def propagate_sigma_pts(self, Chi_x, Chi_u, v, omg):
        v = v + Chi_u[0]
        omg = omg + Chi_u[1]
        th = Chi_x[2]

        th_plus = th + omg * pm.dt
        st = np.sin(th)
        s = np.sin(th_plus)
        ct = np.cos(th)
        c = np.cos(th_plus)

        A = np.array([-v/omg * st + v/omg * s,
                     v/omg * ct - v/omg * c,
                     omg * pm.dt])
        Chix_bar = Chi_x + A

        return Chix_bar

    def augment_state(self, xhat, Sigma, v, omg):
        M = np.diag([pm.alphas[0] * v**2 + pm.alphas[1] * omg**2, 
                    pm.alphas[2] * v**2 + pm.alphas[3] * omg**2])

        xhat_a = np.concatenate((xhat, np.zeros(4)))
        Sig_a = sp.linalg.block_diag(Sigma, M, self.Q)

        return xhat_a, Sig_a

    def generate_sigma_pts(self, xhat_a, L):
        gamma = np.sqrt(self.n + self.lamb)
        Chi_a = np.zeros((self.n, 2 * self.n + 1))

        Chi_a[:,0] = xhat_a
        Chi_a[:,1:self.n+1] = xhat_a.reshape((self.n,1)) + gamma * L
        Chi_a[:, self.n+1:] = xhat_a.reshape((self.n,1)) - gamma * L

        return Chi_a

    def gen_obs_sigmas(self, Chix, Chiz, lmarks_col):
        x, y, th = Chix

        mdx = lmarks_col[0] - x
        mdy = lmarks_col[1] - y
        
        r = np.sqrt( np.add(mdx**2,mdy**2) )
        phi = wrap( np.arctan2(mdy, mdx) - th )

        Z = np.vstack((r, phi)) + Chiz
        return Z
