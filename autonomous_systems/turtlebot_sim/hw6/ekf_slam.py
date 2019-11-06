#! usr/env/python
'''
For this assignment, you are to modify your EKF localization algorithm and simulation to become an EKF SLAM algorithm and simulation.

1) For starters, assume that your sensor is omnidirectional with unlimited range. This means that your sensor can see all landmarks all the time. Show that your EKF SLAM algorithm works by plotting the state estimates (robot pose and landmark locations) against the true states and showing they track/converge. You will likely want to use a few landmarks (<10) to get your algorithm working and debugged. Once it is working, you can increase the number of landmarks. Show that increasing the number of landmarks improves the state estimation accuracy.

2) Plot the final covariance matrix values to illustrate the correlation between landmark states.

3) Narrow the field of view of your sensor to 180 deg, 90 deg, and 45 deg. How does this affect the localization and mapping results? Create an animation of landmark true locations, estimated locations, and estimation covariance (ellipses, 2-sigma) versus time for your simulation.

4) Create a loop-closing scenario with a narrow FOV sensor on your robot. Show how closing the loop (seeing landmarks for second time), results in a drop in landmark location uncertainty for recently viewed landmarks.
tinyurl.com/byurobotgame
'''
import numpy as np
from numpy.linalg import multi_dot
import scipy.linalg as spl

import params as pm
from utils import wrap

class EKF_SLAM():
    def __init__(self):
        self.N = pm.num_lms
        self.dim = 3 + 2*self.N
        self.xhat = np.zeros(self.dim)
        np.concatenate(( pm.state0, pm.lmarks.T.flatten() ), out=self.xhat )
        self.Fx = np.hstack(( np.eye(3), np.zeros((3,2*self.N)) ))
        cols_order = []
        cols = np.arange(self.dim)
        for i in range(self.N):
            cols_select = np.copy(cols)
            k = 2*i-2
            cols_select[3:] = np.roll(cols_select[3:], shift=k)
            cols_order.append(cols_select)
        self.H_inds = np.array(cols_order)
        self.Ha = np.zeros((2,self.dim))

        self.K = np.zeros(3)
        self.R = np.diag([pm.sig_r**2, pm.sig_phi**2])
        self.P = np.eye(3)
        self.Pa = np.zeros((self.dim,self.dim))
        self.Pa[np.diag_indices_from(self.Pa)] = 1e5


        self.Ga = np.eye(self.dim) # Jacobian of g(u_t, x_t-1) wrt state (motion)
        self.V = np.zeros((3,2))  # Jacobian of g(u_t, x_t-1) wrt inputs
        self.M = np.zeros((2,2))  # noise in control space
        self.Qa = np.zeros((self.dim, self.dim))
        self.Ha = np.zeros((2,self.dim))

        # create history arrays
        self.xhat_hist = np.zeros((3, pm.N))
        self.error_cov_hist = np.zeros((3, pm.N))

        self.write_history(0)

    def prediction_step(self, vc, omgc):
        # convenience terms
        th = self.xhat[2]
        th_plus = wrap(th + omgc*pm.dt)
        vo = vc/omgc
        c = np.cos(th) - np.cos(th_plus)
        s = np.sin(th) - np.sin(th_plus)

        ## G matrix ##
        g02 = -vo * c
        g12 = -vo * s
        self.Ga[:2, 2] = [g02, g12]

        # V matrix
        v00 = -s / omgc
        v10 =  c / omgc  
        v01 =  vc*s / omgc**2  +  vc*np.cos(th_plus)*pm.dt / omgc
        v11 = -vc*c / omgc**2  +  vc*np.sin(th_plus)*pm.dt / omgc
        self.V[:] = np.array([[v00, v01],
                              [v10, v11],
                              [  0, pm.dt]])

        # M matrix
        a1, a2, a3, a4 = pm.alphas
        self.M[np.diag_indices_from(self.M)] = [a1*vc**2 + a2*omgc**2, a3*vc**2 + a4*omgc**2]

        # Q matrix
        self.Qa[:3,:3] = multi_dot([self.V, self.M, self.V.T])

        # Prediction state and covariance
        dyn = np.array([-vo*s, vo*c, omgc*pm.dt])
        self.xhat += (self.Fx.T @ dyn)
        self.Pa = multi_dot([self.Ga, self.Pa, self.Ga.T]) + self.Qa

    def measurement_correction(self, r, phi):
        delta = np.zeros(2)
        for i in range(pm.num_lms):
            delta = pm.lmarks[:,i] - self.xhat[:2]
            th = self.xhat[2]
            q = delta @ delta
            r_hat = np.sqrt(q)
            phi_hat = np.arctan2(delta[1], delta[0]) - th

            self.Ha[:,:5] = 1/q * np.hstack((-r_hat*delta, 0, r_hat*delta, 
                                    delta[1], -delta[0], -q, -delta[1], delta[0]
                                    )).reshape(2,5)
            inds = (np.array([0,1]).reshape(2,1), self.H_inds[i]) 
            Ha = self.Ha[inds]
            
            z = np.array([r[i], phi[i]])
            zhat = np.array([r_hat, phi_hat])
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])

            #### Figure out how to update self.Pa(Sigma) ####
            #### Is it just an automatic update? pg. 29 of slides ####
            

            S = multi_dot([Ha, self.Pa, Ha.T]) + self.R
            K = multi_dot([self.Pa, Ha.T, spl.inv(S)])

            self.xhat += K@(zdiff)
            self.Pa = (np.eye(self.dim) - K @ Ha) @ self.Pa

    def write_history(self, i):
        self.xhat_hist[:,i] = self.xhat[:3]
        self.error_cov_hist[:,i] = self.P.diagonal()
