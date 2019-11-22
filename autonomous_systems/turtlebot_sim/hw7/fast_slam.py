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
        self.w = np.ones((self.M))

        self.xhat = np.mean(self.chi_xhat, axis=1)
        
        # self.discovered = np.full(self.N, False)
        self.discovered = np.full(self.N, True)

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
        
        newly_discovered_inds = np.flatnonzero(~self.discovered & detected_mask )
        self.discovered[newly_discovered_inds] = True
        lmarks_new_inds = (np.array([[0],[1]]), newly_discovered_inds)
        
        if len(newly_discovered_inds) > 0:
            # pose init
            r_init, phi_init = z_full[lmarks_new_inds]
            rel_meas = np.stack([r_init*np.cos(phi_init+th), r_init*np.sin(phi_init+th)])
            self.chi_lm[lmarks_new_inds] = self.chi_xhat + rel_meas
            # covariance init
            _, H = self.expected_measurement(self.chi_lm[lmarks_new_inds])
            H_inv = np.linalg.inv(H)
            H_invT = np.transpose(H_inv, (0,2,1))
            self.chi_P[lmarks_new_inds] = H_inv @ self.R @ H_invT

        for j in detected_inds:
            zhat, H = self.expected_measurement(self.chi_lm[j])
            z = np.vstack((r[j], phi[j]))  # (2,M)
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])  #(2,M)
            
            HT = np.transpose(H, (0,2,1))
            S = H @ self.chi_P[j] @ HT + self.R
            S_inv = np.linalg.inv(S)
            K = self.chi_P[j] @ HT @ S_inv

            self.chi_lm[j] += (K@zdiff.T.reshape(self.M,2,1)).squeeze().T
            self.chi_P[j] = (np.eye(2) - K@H) @ self.chi_P[j]

            S_2pi_det = np.linalg.det(2*np.pi*S)
            denom = np.sqrt(S_2pi_det * np.exp(-0.5 * (zdiff.T @ S_inv @ zdiff)))
            res = 1.0/denom
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
 

        temp1 = 1/np.sqrt(2*np.pi*sigs[:,None]**2)
        temp2 = np.exp( -zdiff**2 / (2*sigs[:,None]**2) )
        prob = temp1*temp2
        return np.prod( prob, axis=0 )
    
    def low_variance_sampler(self):
        M_inv = 1/pm.M
        r = np.random.uniform(0, M_inv)
        c = np.cumsum(self.w)
        U = np.arange(pm.M)*M_inv + r
        diff = c - U[:,None]
        inds = np.argmax(diff > 0, axis=1)
        
        return self.Chi[:,inds], inds