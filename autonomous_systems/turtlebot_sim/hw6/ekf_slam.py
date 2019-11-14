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
    import cupy as xp
else:
    import numpy as xp

from utils import wrap

class EKF_SLAM():
    def __init__(self, params):
        self.pm = params
        
        self.N = self.pm.num_lms
        self.dim = 3 + 2*self.N
        self.xhat = xp.zeros(self.dim)
        self.xhat[:3] = xp.array(self.pm.state0)
        self.discovered = xp.full(self.N, False)

        # Eigenv's for covariance ellipses
        self.a = xp.zeros(self.pm.num_lms)
        self.b = xp.array(self.a)
        self.c = xp.array(self.a)
        self.w = xp.zeros((2,self.N))   # eigen values
        self.P_angs = xp.zeros(self.N)  # angle of covar ellipse (from max eigen vec)


        self.Fx = xp.hstack(( xp.eye(3), xp.zeros((3,2*self.N)) ))
        cols_order = []
        cols = xp.arange(self.dim)
        for i in range(1,self.N+1):
            cols_select = xp.copy(cols)
            k = 2*i-2
            cols_select[3:] = xp.roll(cols_select[3:], shift=k)
            cols_order.append(cols_select.tolist())
        self.H_inds = xp.array(cols_order)
        self.Ha = xp.zeros((2,self.dim))

        self.K = xp.zeros(3)
        self.R = xp.diag([self.pm.sig_r**2, self.pm.sig_phi**2])
        self.P = xp.eye(3)
        self.Pa = xp.zeros((self.dim,self.dim))
        pa_init_inds = (xp.arange(3,self.dim), xp.arange(3,self.dim))
        self.Pa[pa_init_inds] = 1e5


        self.Ga = xp.eye(self.dim) # Jacobian of g(u_t, x_t-1) wrt state (motion)
        self.V = xp.zeros((3,2))  # Jacobian of g(u_t, x_t-1) wrt inputs
        self.M = xp.zeros((2,2))  # noise in control space
        self.Qa = xp.zeros((self.dim, self.dim))
        self.Ha = xp.zeros((2,self.dim))

        # create history arrays
        self.xhat_hist = xp.zeros((3, self.pm.N))
        self.error_cov_hist = xp.zeros((2*self.N, self.pm.N))

        self.write_history(0)

    def prediction_step(self, vc, omgc):
        # convenience terms
        th = self.xhat[2]
        th_plus = wrap(th + omgc*self.pm.dt)
        vo = vc/omgc
        c = xp.cos(th) - xp.cos(th_plus)
        s = xp.sin(th) - xp.sin(th_plus)
        vos = vo*s
        voc = vo*c

        ## G matrix ##
        g02 = -voc
        g12 = -vos
        self.Ga[:2, 2] = xp.stack((g02, g12))

        # V matrix
        v00 = -s / omgc
        v10 =  c / omgc  
        v01 =  vc*s / omgc**2  +  vc*xp.cos(th_plus)*self.pm.dt / omgc
        v11 = -vc*c / omgc**2  +  vc*xp.sin(th_plus)*self.pm.dt / omgc
        self.V[:] = xp.stack([xp.stack([v00, v01]),
                              xp.stack([v10, v11]),
                              xp.array([  0, self.pm.dt])])

        # M matrix
        a1, a2, a3, a4 = self.pm.alphas
        self.M[0,0] = a1*vc**2 + a2*omgc**2
        self.M[1,1] = a3*vc**2 + a4*omgc**2

        # Q matrix
        self.Qa[:3,:3] = self.V @ self.M @ self.V.T

        # Prediction state and covariance
        dyn = xp.stack([-vos, voc, omgc*self.pm.dt])
        self.xhat[:3] += dyn
        self.xhat[2] = wrap(self.xhat[2])
        self.Pa = self.Ga @ self.Pa @ self.Ga.T + self.Qa
        
    def measurement_correction(self, z_full, detected_mask):
        r, phi = z_full
        x, y, th = self.xhat[:3]
        detected_inds = xp.flatnonzero(detected_mask)
        
        lmarks_estimates = xp.vstack((self.xhat[3::2], self.xhat[4::2]))
        newly_discovered_inds = xp.flatnonzero(~self.discovered & detected_mask )
        self.discovered[newly_discovered_inds] = True
        lmarks_new_inds = (xp.array([[0],[1]]), newly_discovered_inds)

        if len(newly_discovered_inds) > 0:
            r_init, phi_init = z_full[lmarks_new_inds]
            rel_meas = xp.stack([r_init*xp.cos(phi_init+th), r_init*xp.sin(phi_init+th)])
            lmarks_estimates[lmarks_new_inds] = self.xhat[:2,None] + rel_meas

        self.xhat[3::2] = lmarks_estimates[0]
        self.xhat[4::2] = lmarks_estimates[1]

        
        for i, m in enumerate( detected_inds ):
            delta = lmarks_estimates[:,m] - self.xhat[:2]
            q = delta @ delta
            r_hat = xp.sqrt(q)
            phi_hat = xp.arctan2(delta[1], delta[0]) - th

            self.Ha[:,:5] = 1/q * xp.hstack((-r_hat*delta, 0, r_hat*delta, 
                                             delta[1], -delta[0], -q, -delta[1], delta[0]
                                             )).reshape(2,5)
            inds = (xp.array([0,1]).reshape(2,1), self.H_inds[m]) 
            Ha = self.Ha[inds]
            
            z = xp.stack([r[m], phi[m]])
            zhat = xp.stack([r_hat, phi_hat])
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])
            
            S = Ha @ self.Pa @ Ha.T + self.R
            K = self.Pa @ Ha.T @ xp.linalg.inv(S)

            self.xhat += K@(zdiff)
            self.xhat[2] = wrap(self.xhat[2])
            self.Pa = (xp.eye(self.dim) - K @ Ha) @ self.Pa
        
    def compute_eigs(self):
        # unpack data for discovered landmarks
        p = self.Pa[3:,3:]

        # unpack values of each landmark 2x2 covariance matrix block
        self.a = p.diagonal()[::2][self.discovered]
        self.b = p.diagonal()[1::2][self.discovered]
        self.c = p.ravel()[1::p.shape[0]+1][::2][self.discovered]

        # quadratic formula to find eigenvalues
        q = xp.sqrt( (self.a-self.b)*(self.a-self.b)/4 + self.c*self.c )
        r = (self.a+self.b)/2
        w = xp.vstack([r+q, r-q])

        # setting vx of all eigenvecs as 1, compute vy using eigenvalues (w)
        vy = (w[0]-self.a)/self.c  # only need major eigvec

        # compute angle from x-axis to eigvec pointing along major axis
        # (i.e., eigvec with largest eigval)
        p_angs = xp.arctan(vy)  # arctan(vy/vx), with all vx = 1

        self.w[:,self.discovered] = w
        self.P_angs[self.discovered] = p_angs

    def write_history(self, i):
        self.xhat_hist[:,i] = self.xhat[:3]
        self.error_cov_hist[:,i] = self.Pa.diagonal()[3:]
