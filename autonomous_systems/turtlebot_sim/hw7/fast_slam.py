#! usr/env/python
'''
For this assignment, you are to modify your EKF localization algorithm and simulation to become an EKF SLAM algorithm and simulation.

1) For starters, assume that your sensor is omnidirectional with unlimited range. This means that your sensor can see all landmarks all the time. Show that your EKF SLAM algorithm works by plotting the state estimates (robot pose and landmark locations) against the true states and showing they track/converge. You will likely want to use a few landmarks (<10) to get your algorithm working and debugged. Once it is working, you can increase the number of landmarks. Show that increasing the number of landmarks improves the state estimation accuracy.

2) Plot the final covariance matrix values to illustrate the correlation between landmark states.

3) Narrow the field of view of your sensor to 180 deg, 90 deg, and 45 deg. How does this affect the localization and mapping results? Create an animation of landmark true locations, estimated locations, and estimation covariance (ellipses, 2-sigma) versus time for your simulation.

4) Create a loop-closing scenario with a narrow FOV sensor on your robot. Show how closing the loop (seeing landmarks for second time), results in a drop in landmark location uncertainty for recently viewed landmarks.
'''
import shared

if shared.USE_CUPY:
    import cupy as np
else:
    import numpy as np

from turtlebot import Turtlebot
from utils import wrap

class Fast_SLAM():
    def __init__(self, params):
        self.pm = params
        self.tbot = Turtlebot(self.pm)

        self.N = self.pm.num_lms
        self.M = self.pm.M

        self.chi_xhat = np.zeros((3, self.M))
        self.chi_xhat[:2] = np.random.uniform(-5, 15, (2, self.M))
        self.chi_xhat[2]  = np.random.uniform(-np.pi, np.pi, self.M)

        self.chi_lm = np.zeros((self.N, 2, self.M))
        self.chi_P = np.zeros((self.N, self.M, 2, 2))
        self.w = np.ones(self.M)

        self.P = np.eye(3)
        self.xhat = self.pm.state0
        
        self.discovered = np.full(self.N, False)
        # self.discovered = np.full(self.N, True)

        # Eigenv's for covariance ellipses
        self.a = np.zeros(self.pm.num_lms)
        self.b = np.array(self.a)
        self.c = np.array(self.a)
        self.eigval = np.zeros((2,self.N))   # eigen values
        self.P_angs = np.zeros(self.N)  # angle of covar ellipse (from max eigen vec)


        self.H = np.zeros((self.N, self.M, 2, 2))
        self.K = np.zeros(3)
        self.R = np.diag([self.pm.sig_r**2, self.pm.sig_phi**2])

        # create history arrays
        self.xhat_hist = np.zeros((3, self.pm.N))
        self.error_cov_hist = np.zeros((2*self.N, self.pm.N))

        # self.write_history(0)

    def prediction_step(self, vc, omgc):
        self.chi_xhat = self.tbot.sample_motion_model(
            vc, omgc, self.chi_xhat, particles=True)

    def measurement_correction(self, z_full, detected_mask):

        r, phi = z_full  # r: (N), phi (N)
        x, y, th = self.chi_xhat  # (3, M)
        detected_inds = np.flatnonzero(detected_mask)
        
        new_discovered_inds = np.flatnonzero(~self.discovered & detected_mask )
        self.discovered[new_discovered_inds] = True
        new_inds_tup = (np.array([0,1]).reshape(2,1), new_discovered_inds)
        
        if len(new_discovered_inds) > 0:
            # pose init
            r_init, phi_init = np.tile(z_full[:,:,None],self.M)  # (N,M)
            x = r_init*np.cos( phi_init+th ) # (N,M)
            y = r_init*np.sin( phi_init+th )
            rel_meas = np.stack((x, y), axis=1) # (N,2,M)<--(x dist, y dist)
            # chi_lm_init = self.chi_xhat[:2] + rel_meas  # (2,M)
            # self.chi_lm = chi_lm_init
            self.chi_lm = self.chi_xhat[:2] + rel_meas  # (2,M)
            # covariance init
            for j in new_discovered_inds:
                _, H = self.expected_measurement(self.chi_lm[j])
                H_inv = np.linalg.inv(H)
                H_invT = np.transpose(H_inv, (0,2,1))
                self.chi_P[j] = H_inv @ self.R @ H_invT

        self.w = np.ones(,self.M)
        for j in detected_inds:
            zhat, H = self.expected_measurement(self.chi_lm[j])
            z = np.vstack((r[j], phi[j]))  # (2,M)
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])
            # resizing zdiff for matmul
            zdiff = zdiff.T.reshape(self.M,2,1)  #(M,2,1)
            zdiffT = np.transpose(zdiff, (0,2,1))

            HT = np.transpose(H, (0,2,1))
            S = H @ self.chi_P[j] @ HT + self.R
            S_inv = np.linalg.inv(S)
            K = self.chi_P[j] @ HT @ S_inv

            self.chi_lm[j] += (K @ zdiff).squeeze().T
            self.chi_P[j] = (np.eye(2) - K@H) @ self.chi_P[j]

            S_2pi_det = np.linalg.det(2*np.pi*S)
            zs = (zdiffT @ S_inv @ zdiff).squeeze()
            res = 1.0/np.sqrt(S_2pi_det) * np.exp( -0.5*zs )
            self.w *= res
        wsum = np.sum(self.w)
        wsum_inv = 1/wsum
        self.w *= wsum_inv

    def expected_measurement(self, lmj):
        th = self.chi_xhat[2]

        delta = lmj - self.chi_xhat[:2]  # (2,M)
        q = delta[0]**2 + delta[1]**2    # (M)
        r_hat = np.sqrt(q)               # (M)
        phi_hat = np.arctan2(delta[1], delta[0]) - th  # (M)
        zhat = np.vstack((r_hat, phi_hat))  # (2,M)
        
        a = -delta[0]/r_hat
        b = -delta[1]/r_hat
        c = delta[1]/q
        d = delta[0]/q
        H = np.array([a,b,c,d]).reshape(self.M,2,2)
        return zhat, H
 
    def low_variance_sampler(self):
        M_inv = 1/self.M
        r = np.random.uniform(0, M_inv)
        c = np.cumsum(self.w)
        U = np.arange(self.M)*M_inv + r
        diff = c - U[:,None]
        inds = np.argmax(diff > 0, axis=1)

        self.xhat = np.mean(self.chi_xhat, axis=1) 


        est_errors = self.chi_xhat - self.xhat[:,None]
        est_errors[2] = wrap(est_errors[2])
        # np.cov is equivalent to P = np.mean(self.w) * est_errors @ est_errors.T
        self.P = np.cov(est_errors)
        uniq = len(np.unique(inds))
        if uniq/self.M < 0.5:
            Q = self.P / (self.M*uniq)**(1/3)
            self.chi_xhat += Q @ np.random.randn(*self.chi_xhat.shape)
        
    def compute_eigs(self):
        # unpack data for discovered landmarks
        p = self.chi_P[3:,3:]

        # unpack values of each landmark 2x2 covariance matrix block
        self.a = p.diagonal()[::2][self.discovered]
        self.b = p.diagonal()[1::2][self.discovered]
        self.c = p.ravel()[1::p.shape[0]+1][::2][self.discovered]

        # quadratic formula to find eigenvalues
        q = np.sqrt( (self.a-self.b)*(self.a-self.b)/4 + self.c*self.c )
        r = (self.a+self.b)/2
        w = np.vstack([r+q, r-q])

        # setting vx of all eigenvecs as 1, compute vy using eigenvalues (w)
        vy = (w[0]-self.a)/self.c  # only need major eigvec

        # compute angle from x-axis to eigvec pointing along major axis
        # (i.e., eigvec with largest eigval)
        p_angs = np.arctan(vy)  # arctan(vy/vx), with all vx = 1

        self.w[:,self.discovered] = w
        self.P_angs[self.discovered] = p_angs

    def write_history(self, i):
        self.xhat_hist[:,i] = self.xhat[:3]
        self.error_cov_hist[:,i] = self.Pa.diagonal()[3:]
