#! usr/env/python
'''
For this assignment, you are to implement the Fast SLAM algorithm (Table 13.1) on the same landmark world that you used for the EKF SLAM assignment. 

1) For starters, assume that your sensor is omnidirectional with unlimited range. This means that your sensor can see all landmarks from any place in the environment. Keep in mind that the FastSLAM algorithm that we implement assumes that only a single feature is measured at each point in time. Show that your Fast SLAM algorithm works by plotting the state estimates (robot pose and landmark locations) against the true states and showing they track/converge. You will likely want to use a few landmarks (<10) to get your algorithm working and debugged. Once it is working, you can increase the number of landmarks. Show that increasing the number of landmarks improves the state estimation accuracy.

2) Narrow the field of view of your sensor to 180 deg, 90 deg, and 45 deg. How does this affect the localization and mapping results? Create an animation of landmark true locations, estimated locations, and estimation covariance (ellipses, 2-sigma) versus time for your simulation.

3) Compare the performance of your Fast SLAM algorithm to that of your EKF SLAM algorithm. How do they compare as you increase the level of your linear and angular input velocity uncertainties are increased?

'''
import cupy as cp

from utils import wrap

class FastSLAM():
    def __init__(self, params):
        self.pm = params
        
        self.N = self.pm.num_lms
        self.dim = 3 + 2*self.N
        self.xhat = cp.zeros(self.dim)
        self.xhat[:3] = cp.array(self.pm.state0)
        self.discovered = cp.full(self.N, False)

        # Eigenv's for covariance ellipses
        self.a = cp.zeros(self.pm.num_lms)
        self.b = cp.array(self.a)
        self.c = cp.array(self.a)
        self.w = cp.zeros((2,self.N))   # eigen values
        self.P_angs = cp.zeros(self.N)  # angle of covar ellipse (from max eigen vec)


        self.Fx = cp.hstack(( cp.eye(3), cp.zeros((3,2*self.N)) ))
        cols_order = []
        cols = cp.arange(self.dim)
        for i in range(1,self.N+1):
            cols_select = cp.copy(cols)
            k = 2*i-2
            cols_select[3:] = cp.roll(cols_select[3:], shift=k)
            cols_order.append(cols_select.tolist())
        self.H_inds = cp.array(cols_order)
        self.Ha = cp.zeros((2,self.dim))

        self.K = cp.zeros(3)
        self.R = cp.diag([self.pm.sig_r**2, self.pm.sig_phi**2])
        self.P = cp.eye(3)
        self.Pa = cp.zeros((self.dim,self.dim))
        pa_init_inds = (cp.arange(3,self.dim), cp.arange(3,self.dim))
        self.Pa[pa_init_inds] = 1e5


        self.Ga = cp.eye(self.dim) # Jacobian of g(u_t, x_t-1) wrt state (motion)
        self.V = cp.zeros((3,2))  # Jacobian of g(u_t, x_t-1) wrt inputs
        self.M = cp.zeros((2,2))  # noise in control space
        self.Qa = cp.zeros((self.dim, self.dim))
        self.Ha = cp.zeros((2,self.dim))

        # create history arrays
        self.xhat_hist = cp.zeros((3, self.pm.N))
        self.error_cov_hist = cp.zeros((2*self.N, self.pm.N))

        self.write_history(0)

    def prediction_step(self, vc, omgc):
        # convenience terms
        th = self.xhat[2]
        th_plus = wrap(th + omgc*self.pm.dt)
        vo = vc/omgc
        c = cp.cos(th) - cp.cos(th_plus)
        s = cp.sin(th) - cp.sin(th_plus)
        vos = vo*s
        voc = vo*c

        ## G matrix ##
        g02 = -voc
        g12 = -vos
        self.Ga[:2, 2] = cp.stack((g02, g12))

        # V matrix
        v00 = -s / omgc
        v10 =  c / omgc  
        v01 =  vc*s / omgc**2  +  vc*cp.cos(th_plus)*self.pm.dt / omgc
        v11 = -vc*c / omgc**2  +  vc*cp.sin(th_plus)*self.pm.dt / omgc
        self.V[:] = cp.stack([cp.stack([v00, v01]),
                              cp.stack([v10, v11]),
                              cp.array([  0, self.pm.dt])])

        # M matrix
        a1, a2, a3, a4 = self.pm.alphas
        self.M.diagonal()[:] = cp.stack([a1*vc**2 + a2*omgc**2, a3*vc**2 + a4*omgc**2])

        # Q matrix
        self.Qa[:3,:3] = self.V @ self.M @ self.V.T

        # Prediction state and covariance
        dyn = cp.stack([-vos, voc, omgc*self.pm.dt])
        self.xhat[:3] += dyn
        self.xhat[2] = wrap(self.xhat[2])
        self.Pa = self.Ga @ self.Pa @ self.Ga.T + self.Qa

    def measurement_correction(self, z_full, detected_mask):
        r, phi = z_full
        x, y, th = self.xhat[:3]
        detected_inds = cp.flatnonzero(detected_mask)
        
        lmarks_estimates = cp.vstack((self.xhat[3::2], self.xhat[4::2]))
        newly_discovered_inds = cp.flatnonzero(~self.discovered & detected_mask )
        self.discovered[newly_discovered_inds] = True
        lmarks_new_inds = (cp.array([[0],[1]]), newly_discovered_inds)

        if len(newly_discovered_inds) > 0:
            r_init, phi_init = z_full[lmarks_new_inds]
            rel_meas = cp.stack([r_init*cp.cos(phi_init+th), r_init*cp.sin(phi_init+th)])
            lmarks_estimates[lmarks_new_inds] = self.xhat[:2,None] + rel_meas

        self.xhat[3::2] = lmarks_estimates[0]
        self.xhat[4::2] = lmarks_estimates[1]

        
        for i, m in enumerate( detected_inds ):
            delta = lmarks_estimates[:,m] - self.xhat[:2]
            q = delta @ delta
            r_hat = cp.sqrt(q)
            phi_hat = cp.arctan2(delta[1], delta[0]) - th

            self.Ha[:,:5] = 1/q * cp.hstack((-r_hat*delta, 0, r_hat*delta, 
                                             delta[1], -delta[0], -q, -delta[1], delta[0]
                                             )).reshape(2,5)
            inds = (cp.array([0,1]).reshape(2,1), self.H_inds[m]) 
            Ha = self.Ha[inds]
            
            z = cp.stack([r[m], phi[m]])
            zhat = cp.stack([r_hat, phi_hat])
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])
            
            S = Ha @ self.Pa @ Ha.T + self.R
            K = self.Pa @ Ha.T @ cp.linalg.inv(S)

            self.xhat += K@(zdiff)
            self.xhat[2] = wrap(self.xhat[2])
            self.Pa = (cp.eye(self.dim) - K @ Ha) @ self.Pa
        
    def compute_eigs(self):
        # unpack data for discovered landmarks
        p = self.Pa[3:,3:]

        # unpack values of each landmark 2x2 covariance matrix block
        self.a = p.diagonal()[::2][self.discovered]
        self.b = p.diagonal()[1::2][self.discovered]
        self.c = p.ravel()[1::p.shape[0]+1][::2][self.discovered]

        # quadratic formula to find eigenvalues
        q = cp.sqrt( (self.a-self.b)*(self.a-self.b)/4 + self.c*self.c )
        r = (self.a+self.b)/2
        w = cp.vstack([r+q, r-q])

        # setting vx of all eigenvecs as 1, compute vy using eigenvalues (w)
        vy = (w[0]-self.a)/self.c  # only need major eigvec

        # compute angle from x-axis to eigvec pointing along major axis
        # (i.e., eigvec with largest eigval)
        p_angs = cp.arctan(vy)  # arctan(vy/vx), with all vx = 1

        self.w[:,self.discovered] = w
        self.P_angs[self.discovered] = p_angs

    def write_history(self, i):
        self.xhat_hist[:,i] = self.xhat[:3]
        self.error_cov_hist[:,i] = self.Pa.diagonal()[3:]
