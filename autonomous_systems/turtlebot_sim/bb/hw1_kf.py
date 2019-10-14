from IPython.core.debugger import set_trace
from importlib import reload

import numpy as np
import scipy as sp

class UUV():
    def init():
        # belief of correction
        self.mu_bar_t = None
        self.sigma_bar_t = None

        # belief of prediction
        self.mu_t = None
        self.sigma_t = None
        # initialize
        self.mu_tm1 = 0
        self.sigma_tm1 = 1
    #
    def kf_run():
        for ii in range(self.t0,self.t3,self.dt):
            if ii < self.t1:
                uu_t = self.F_nom
            elif self.t1 < ii < self.t2:
                uu_t = 0
            else:
                uu_t = -self.F_nom
            #
            zz_t = None

            self.kf_predict(uu_t)
            self.kf_gain()
            self.kf_correct(zz_t)

            self.mu_tm1 = self.mu_t
            self.sigma_tm1 = self.sigma_t
        #
    #
    def kf_predict(self, uu_t):
        self.mu_bar_t = np.dot(self.A_dz, self.mu_tm1) + np.dot(self.B_dz, uu_t)

        sigtm1_AT = np.dot(self.sigma_tm1, self.A_dz.T)
        self.sigma_bar_t = np.dot(self.A_dz, sigtm1_AT) + self.Q_t
    #
    def kf_gain(self):
        # Kalman gain
        # compute numerator
        sigb_CT = np.dot(self.sigma_bar_t, self.C_dz.T)
        # compute denominator
        C_sigb_CT = np.dot(self.C_dz, sigb_CT)
        C_sigb_CT_pR = C_sigb_CT + self.R_t
        # solve Kalman
        self.K_t = sp.linalg.solve(C_sigb_CT_pR, sigb_CT).T
    #
    def kf_correct(self, zz_t):
        z_C_mub = zz_t - np.dot(self.C_dz, self.mu_bar_t)
        self.mu_t = self.mu_bar_t + np.dot(self.K_t, z_C_mub)

        eye_K_C = np.eye(2) - np.dot(self.K_t, self.C_dz)
        self.sigma_t = np.dot(eye_K_C, self.sigma_bar_t)
        #
    #


#
