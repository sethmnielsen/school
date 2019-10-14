from IPython.core.debugger import set_trace
# import importlib as imp
from importlib import reload

import numpy as np
import scipy as sp
# import scipy.io as scio

import lmd
reload(lmd)

class Ekf():
    def __init__(self, tbot):

        self.tbot = tbot
        self.uu_hist = tbot.uu_des_hist__np
        self.zz_hist = tbot.zz_hist__np
        self.lm_all = tbot.lm_all
        self.dt = tbot.dt
        self.t_span = tbot.t_span
        self.num_t_pts = tbot.num_t_pts

        self.mu = np.array([0.,0.,0.])
        self.sigma = np.array(np.diag([1.,1.,1.]))

        self.Q_t = np.array([[self.tbot.sigma_r**2, 0],[0, self.tbot.sigma_phi**2]])

        self.mu_hist = []
        self.sigma_hist = []
        self.K_hist = []
    #
    def ekf_localize(self):
        for ii in range(self.num_t_pts):
            uu = self.uu_hist[:,ii]
            zz = self.zz_hist[ii]
            self.prediction(uu)

            # self.kalman_gain_up()

            self.correction(zz)

            self.mu_hist.append(self.mu)
            self.sigma_hist.append(self.sigma)
        #
        self.mu_hist = np.asarray(self.mu_hist).T
        self.sigma_hist = np.asarray(self.sigma_hist)
        self.K_hist = np.asarray(self.K_hist)
    #
    def prediction(self, uu):
        vv = uu[0]
        ww = uu[1]
        ww_inv = 1 / ww
        ww_inv_sq = 1 / ww_inv

        psi = self.mu[2]

        v_w_inv = vv * ww_inv
        psi_omega_dt = lmd.rad_wrap_pi(psi + ww*self.dt)

        cps = np.cos(psi)
        sps = np.sin(psi)
        cpsw = np.cos(psi_omega_dt)
        spsw = np.sin(psi_omega_dt)

        pcos_ncos = cps - cpsw
        nsin_psin = -sps + spsw

        pcos_ncos_w_inv = pcos_ncos * ww_inv
        nsin_psin_w_inv = nsin_psin * ww_inv

        # ===



        # ==============================

        G_t = np.array([[1,0,-v_w_inv * pcos_ncos], [0,1,v_w_inv * nsin_psin],[0,0,1]])

        V_t = np.array([[nsin_psin_w_inv, v_w_inv * (-nsin_psin_w_inv + cpsw * self.dt)], [pcos_ncos_w_inv, v_w_inv * (-pcos_ncos_w_inv + spsw * self.dt)], [0, self.dt]])

        M_t = np.array([[self.tbot.alpha1*vv**2 + self.tbot.alpha2*ww**2, 0], [0, self.tbot.alpha3*vv**2 + self.tbot.alpha4*ww**2]])

        mu_bar_vec = np.array([v_w_inv * nsin_psin, v_w_inv * pcos_ncos, ww * self.dt])

        self.mu_bar = self.mu + mu_bar_vec
        self.sigma_bar = G_t @ self.sigma @ G_t.T + V_t @ M_t @ V_t.T

    #
    def kalman_gain_up(self):
        pass
    #
    def correction(self, zz):

        z_hat = np.zeros((2,self.tbot.num_lm))

        # z_sub = np.zeros((2,3))
        p_zt = 1

        if self.tbot.num_lm == 1:
            tmp_lm_all = np.array([self.lm_all]).T
        else:
            tmp_lm_all = self.lm_all
        #

        # for ii in range(self.tbot.num_lm):
        for ii, lm_ii in enumerate(tmp_lm_all.T):

            # set_trace()

            zz_ii = zz[:,ii]
            # m subtract mu_bar
            m_s_mub = lm_ii - self.mu_bar[0:2]
            # m_s_mub = (self.lm_all.T[0:2,ii] - self.mu_bar[0:2]).T
            # set_trace()
            qq = np.sum((m_s_mub)**2)
            sqrt_qq = np.sqrt(qq)
            qq_inv = 1 / qq
            sqrt_qq_inv = 1 / sqrt_qq

            # set_trace()
            z_hat[:,ii] = np.array([sqrt_qq, lmd.rad_wrap_pi(np.arctan2(m_s_mub[1],m_s_mub[0]) - self.mu_bar[2])])

            H_t = np.array([[-m_s_mub[0] * sqrt_qq_inv, -m_s_mub[1] * sqrt_qq_inv, 0], [m_s_mub[1] * qq_inv, -m_s_mub[0] * qq_inv, -1]])

            S_t = H_t @ self.sigma_bar @ H_t.T + self.Q_t
            K_t = self.sigma_bar @ H_t.T @ np.linalg.inv(S_t)

            z_subtract = zz_ii - z_hat[:,ii]
            z_subtract[1] = lmd.rad_wrap_pi(z_subtract[1])

            # p_zt *= np.det()

            self.mu_bar = self.mu_bar + K_t @ (z_subtract)
            self.mu_bar[2] = lmd.rad_wrap_pi(self.mu_bar[2])
            self.sigma_bar = (lmd.eye3 - K_t @ H_t) @ self.sigma_bar

            self.K_hist.append(K_t)
        #
        self.mu = self.mu_bar
        self.sigma = self.sigma_bar
    #

#
