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

from utils import wrap

class Fast_SLAM():
    def __init__(self, params):
        self.pm = params

        self.N = self.pm.num_lms
        self.M = self.pm.M

        self.Chi = np.zeros((3,pm.Mh))
        self.Chi[:2] = np.random.uniform(-10, 10, (2, self.M))
        self.Chi[2]  = np.random.uniform(-np.pi, np.pi, self.M)

        self.xhat = np.mean(self.Chi, axis=1)
        x_errors = wrap(self.Chi - self.xhat[:,None], dim=2)
        self.P = np.cov(x_errors)
        
        self.dim = 3 + 2*self.N
        self.xhat = np.zeros(self.dim)
        self.xhat[:3] = np.array(self.pm.state0)
        self.discovered = np.full(self.N, False)

        # Eigenv's for covariance ellipses
        self.a = np.zeros(self.pm.num_lms)
        self.b = np.array(self.a)
        self.c = np.array(self.a)
        self.w = np.zeros((2,self.N))   # eigen values
        self.P_angs = np.zeros(self.N)  # angle of covar ellipse (from max eigen vec)


        self.Fx = np.hstack(( np.eye(3), np.zeros((3,2*self.N)) ))
        cols_order = []
        cols = np.arange(self.dim)
        for i in range(1,self.N+1):
            cols_select = np.copy(cols)
            k = 2*i-2
            cols_select[3:] = np.roll(cols_select[3:], shift=k)
            cols_order.append(cols_select.tolist())
        self.H_inds = np.array(cols_order)
        self.Ha = np.zeros((2,self.dim))

        self.K = np.zeros(3)
        self.R = np.diag([self.pm.sig_r**2, self.pm.sig_phi**2])
        self.P = np.eye(3)
        self.Pa = np.zeros((self.dim,self.dim))
        pa_init_inds = (np.arange(3,self.dim), np.arange(3,self.dim))
        self.Pa[pa_init_inds] = 1e5


        self.Ga = np.eye(self.dim) # Jacobian of g(u_t, x_t-1) wrt state (motion)
        self.V = np.zeros((3,2))  # Jacobian of g(u_t, x_t-1) wrt inputs
        self.M = np.zeros((2,2))  # noise in control space
        self.Qa = np.zeros((self.dim, self.dim))
        self.Ha = np.zeros((2,self.dim))

        # create history arrays
        self.xhat_hist = np.zeros((3, self.pm.N))
        self.error_cov_hist = np.zeros((2*self.N, self.pm.N))

        self.write_history(0)

    def prediction_step(self, vc, omgc):
        # convenience terms
        th = self.xhat[2]
        th_plus = wrap(th + omgc*self.pm.dt)
        vo = vc/omgc
        c = np.cos(th) - np.cos(th_plus)
        s = np.sin(th) - np.sin(th_plus)
        vos = vo*s
        voc = vo*c

        ## G matrix ##
        g02 = -voc
        g12 = -vos
        self.Ga[:2, 2] = np.stack((g02, g12))

        # V matrix
        v00 = -s / omgc
        v10 =  c / omgc  
        v01 =  vc*s / omgc**2  +  vc*np.cos(th_plus)*self.pm.dt / omgc
        v11 = -vc*c / omgc**2  +  vc*np.sin(th_plus)*self.pm.dt / omgc
        self.V[:] = np.stack([np.stack([v00, v01]),
                              np.stack([v10, v11]),
                              np.array([  0, self.pm.dt])])

        # M matrix
        a1, a2, a3, a4 = self.pm.alphas
        self.M[0,0] = a1*vc**2 + a2*omgc**2
        self.M[1,1] = a3*vc**2 + a4*omgc**2

        # Q matrix
        self.Qa[:3,:3] = self.V @ self.M @ self.V.T

        # Prediction state and covariance
        dyn = np.stack([-vos, voc, omgc*self.pm.dt])
        self.xhat[:3] += dyn
        self.xhat[2] = wrap(self.xhat[2])
        self.Pa = self.Ga @ self.Pa @ self.Ga.T + self.Qa
        
    def measurement_correction(self, z_full, detected_mask):
        r, phi = z_full
        x, y, th = self.xhat[:3]
        detected_inds = np.flatnonzero(detected_mask)
        
        lmarks_estimates = np.vstack((self.xhat[3::2], self.xhat[4::2]))
        newly_discovered_inds = np.flatnonzero(~self.discovered & detected_mask )
        self.discovered[newly_discovered_inds] = True
        lmarks_new_inds = (np.array([[0],[1]]), newly_discovered_inds)

        if len(newly_discovered_inds) > 0:
            r_init, phi_init = z_full[lmarks_new_inds]
            rel_meas = np.stack([r_init*np.cos(phi_init+th), r_init*np.sin(phi_init+th)])
            lmarks_estimates[lmarks_new_inds] = self.xhat[:2,None] + rel_meas

        self.xhat[3::2] = lmarks_estimates[0]
        self.xhat[4::2] = lmarks_estimates[1]

        
        for i, m in enumerate( detected_inds ):
            delta = lmarks_estimates[:,m] - self.xhat[:2]
            q = delta @ delta
            r_hat = np.sqrt(q)
            phi_hat = np.arctan2(delta[1], delta[0]) - th

            self.Ha[:,:5] = 1/q * np.hstack((-r_hat*delta, 0, r_hat*delta, 
                                             delta[1], -delta[0], -q, -delta[1], delta[0]
                                             )).reshape(2,5)
            inds = (np.array([0,1]).reshape(2,1), self.H_inds[m]) 
            Ha = self.Ha[inds]
            
            z = np.stack([r[m], phi[m]])
            zhat = np.stack([r_hat, phi_hat])
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])
            
            S = Ha @ self.Pa @ Ha.T + self.R
            K = self.Pa @ Ha.T @ np.linalg.inv(S)

            self.xhat += K@(zdiff)
            self.xhat[2] = wrap(self.xhat[2])
            self.Pa = (np.eye(self.dim) - K @ Ha) @ self.Pa
        
    def compute_eigs(self):
        # unpack data for discovered landmarks
        p = self.Pa[3:,3:]

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
