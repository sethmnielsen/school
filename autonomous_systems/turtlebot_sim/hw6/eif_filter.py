aimport numpy as np
import params as pm
import scipy.linalg as spl
from utils import wrap


class EIF():
    
    def __init__(self):
        self.xhat = np.array([pm.x0, pm.y0, pm.th0])
        self.xbar = np.zeros(3)

        # time
        self.marks = np.zeros((2,6))

        # Noise
        self.R = np.diag([pm.sig_r**2, pm.sig_phi**2])

        self.OM = np.eye(3)
        self.OMbar = np.eye(3)
        self.ksi = np.array(pm.state0)
        self.ksi_bar = np.array(pm.state0)

        # create history arrays
        self.x_truth = np.zeros((3, pm.N))
        self.ksi_hist = np.zeros((3, pm.N))
        self.xhat_hist = np.zeros((3, pm.N))
        self.error_cov_hist = np.zeros((3, pm.N))

        self.write_history(0)

    def prediction_step(self, vc, omgc):
        self.xhat = spl.solve(self.OM, self.ksi)
        self.xhat[2] = wrap(self.xhat[2])
        
        # G = np.eye(3)        # Jacobian of g(u_t, x_t-1) wrt state
        # V = np.zeros((3,2))  # Jacobian of g(u_t, x_t-1) wrt inputs
        # M = np.zeros((2,2))  # noise in control space

        eps = np.array([pm.sig_v, pm.sig_omg]) * np.random.randn(2)
        v_n, omg_n = np.array([vc, omgc]) + eps

        M = np.array([[v_n, 0],
                      [0, omg_n]])

        th_hat = self.xhat[2]
        G = np.array([[1, 0, -vc*np.sin(th_hat)],
                      [0, 1,  vc*np.cos(th_hat)],
                      [0, 0,  1]])
        
        V = np.array([[np.cos(th_hat), 0],
                      [np.sin(th_hat), 0],
                      [0             , 1]])

        G[np.abs(G)<1e-6] = 0.
        V[np.abs(V)<1e-6] = 0.
        
        dyn = np.array([vc*np.cos(th_hat), vc*np.sin(th_hat), omgc]) * pm.dt
        self.xbar = self.xhat + dyn
        self.xbar[np.abs(self.xbar)<1e-6] = 0.
        self.xbar[2] = wrap(self.xbar[2])
        self.OMbar = spl.inv( G @ spl.solve(self.OM, G.T) + V @ M @ V.T )
        self.ksi_bar = self.OMbar @ self.xbar

    def measurement_correction(self, r, phi):
        for i in range(pm.num_lms):
            mdx = self.marks[0,i] - self.xbar[0]
            mdy = self.marks[1,i] - self.xbar[1]
            th = self.xbar[2]
            q = mdx**2 + mdy**2
            r_hat = np.sqrt(q)
            phi_hat = np.arctan2(mdy, mdx) - th
            H = np.array([[-mdx/r_hat, -mdy/r_hat,  0],
                          [ mdy/q, -mdx/q, -1]])


            z = np.array([r[i], phi[i]])
            zhat = np.array([r_hat, phi_hat]) + np.diag(self.R)
            zdiff = z - zhat
            zdiff[1] = wrap(zdiff[1])

            self.OMbar += H.T @ spl.solve(self.R, H)
            self.ksi_bar += H.T @ spl.solve(self.R, zdiff + H @ self.xbar )
        
        self.OM = self.OMbar
        self.ksi = self.ksi_bar

    def write_history(self, i):
        self.ksi_hist[:,i] = self.ksi
        self.xhat_hist[:,i] = self.xhat
        self.error_cov_hist[:,i] = spl.inv(self.OM).diagonal()
    
