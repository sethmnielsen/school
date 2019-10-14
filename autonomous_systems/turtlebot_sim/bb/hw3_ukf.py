from IPython.core.debugger import set_trace
# import importlib as imp
from importlib import reload

import numpy as np
import scipy as sp
# import scipy.io as scio
import scipy.linalg

import pandas as pd
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

import lmd
reload(lmd)

class Ukf():
    def __init__(self, tbot):

        self.tbot = tbot
        self.uu_hist = tbot.uu_des_hist__np
        self.zz_hist = tbot.zz_hist__np
        self.num_lm = tbot.num_lm
        self.lm_all = tbot.lm_all
        self.dt = tbot.dt
        self.t_span = tbot.t_span
        self.num_t_pts = tbot.num_t_pts

        self.mu = np.array([0.,0.,0.])
        self.mu = tbot.xx0_perf
        self.sigma = np.eye(3) * 0.1

        self.Q_t = np.array([[self.tbot.sigma_r**2, 0],[0, self.tbot.sigma_phi**2]])

        self.mu_hist = []
        self.sigma_hist = []
        self.K_hist = []

        # ===
        self.dim_gauss = 7

        self.beta_sig_pt = 2
        self.alpha_sig_pt = 0.4
        self.kappa = 4
        self.lambda_ukf = self.alpha_sig_pt**2 * (self.dim_gauss + self.kappa) - self.dim_gauss
        self.gamma = np.sqrt(self.dim_gauss + self.lambda_ukf)

        self.wght_m_0 = self.lambda_ukf / (self.dim_gauss + self.lambda_ukf)
        self.wght_c_0 = self.wght_m_0 + (1 - self.alpha_sig_pt**2 + self.beta_sig_pt)

        self.wght_m_ii = [0.5 / (self.dim_gauss + self.lambda_ukf)] * 2*self.dim_gauss
        self.wght_c_ii = self.wght_m_ii

        self.wght_m = np.array([self.wght_m_0] + self.wght_m_ii)
        self.wght_c = np.array([self.wght_c_0] + self.wght_c_ii)
        # set_trace()
        # ===

        self.mu_a = np.zeros(self.dim_gauss)
        self.sigma_a = np.zeros((self.dim_gauss, self.dim_gauss))


    #
    def ukf_localize(self):
        for ii in range(self.num_t_pts):
            uu = self.uu_hist[:,ii]
            zz = self.zz_hist[ii]
            # set_trace()
            if self.num_lm == 1:
                self.lm_ii = self.lm_all
            else:
                self.lm_ii = self.lm_all.T[0]
            #
            self.lm_idx = 0

            self.prediction(uu)
            self.correction(zz)
            # self.correction(zz, self.mu_bar, self.sigma_bar)

            if self.num_lm > 1:
                for ii in range(1,self.num_lm):
                    self.lm_idx = ii
                    self.lm_ii = self.lm_all.T[ii]
                    self.loop_extra_landmarks(zz)
                #
            #

            # set_trace()

            self.mu_hist.append(self.mu)
            self.sigma_hist.append(self.sigma)
        #
        self.mu_hist = np.asarray(self.mu_hist).T
        self.sigma_hist = np.asarray(self.sigma_hist)
        self.K_hist = np.asarray(self.K_hist)
    #
    def prediction(self, uu):
        self.calc_M_t(uu)

        self.build_mu_sigma_a()

        self.generate_sig_points()

        self.calc_chi_bar_x(uu)

        self.calc_mu_sig_bars()

        # self.
    #
    def calc_M_t(self, uu):
        vv = uu[0]
        ww = uu[1]
        ww_inv = 1 / ww
        ww_inv_sq = 1 / ww_inv

        # psi = self.mu[2]

        # ==============================

        self.M_t = np.array([[self.tbot.alpha1*vv**2 + self.tbot.alpha2*ww**2, 0], [0, self.tbot.alpha3*vv**2 + self.tbot.alpha4*ww**2]])
    #

    def build_mu_sigma_a(self):
        self.mu_a[0:3] = self.mu
        self.sigma_a[0:3,0:3] = self.sigma
        self.sigma_a[3:5,3:5] = self.M_t
        self.sigma_a[5:,5:] = self.Q_t
    #

    def generate_sig_points(self):
        sqrt_sigma_a = sp.linalg.cholesky(self.sigma_a, lower=True)
        # gamma = 1
        gamma_sqrt_sigma_a = self.gamma * sqrt_sigma_a
        mup = self.mu_a[:,None] + gamma_sqrt_sigma_a
        mum = self.mu_a[:,None] - gamma_sqrt_sigma_a

        # set_trace()
        # mu_a needs to be a column vector
        self.chi_a = np.hstack((self.mu_a[:,None], mup, mum))
        self.chi_a[2] = lmd.rad_wrap_pi(self.chi_a[2])
        # self.chi_a[4] = lmd.rad_wrap_pi(self.chi_a[4])
        self.chi_a[6] = lmd.rad_wrap_pi(self.chi_a[6])

        self.chi_x = self.chi_a[0:3]
        self.chi_u = self.chi_a[3:5]
        self.chi_z = self.chi_a[5:]
    #
    def calc_chi_bar_x(self, uu):
        # set_trace()
        self.chi_x_bar = self.tbot.propagate_motion_model(uu[:,None]+self.chi_u, self.chi_x, noise=0)
    #
    def calc_mu_sig_bars(self):

        # set_trace()

        self.mu_bar = self.chi_x_bar @ self.wght_m
        self.mu_bar[2] = lmd.rad_wrap_pi(self.mu_bar[2])

        chi_xmmu_bars = self.chi_x_bar - self.mu_bar[:,None]
        chi_xmmu_bars[2] = lmd.rad_wrap_pi(chi_xmmu_bars[2])
        # TODO: Wrong???
        self.sigma_bar = (chi_xmmu_bars * self.wght_c) @ chi_xmmu_bars.T

        # self.chi_xmmu_bars = chi_xmmu_bars
    #

    # def correction(self, zz, mu_bar, sigma_bar):
    def correction(self, zz):
        # z_hat = np.zeros((2,3))

        # set_trace()

        # for lm_ii in self.lm_all:
        self.calc_zz_ukf(self.lm_ii)
        # self.zz_bar = self.tbot.calc_zz(self.chi_x_bar, lm_ii, noise=0)
        # self.calc_zz_ukf()
        Z_bar = self.zz_bar + self.chi_z
        Z_bar[1] = lmd.rad_wrap_pi(Z_bar[1])
        z_hat = Z_bar @ self.wght_m
        z_hat[1] = lmd.rad_wrap_pi(z_hat[1])

        Zbar_m_zhat = Z_bar - z_hat[:,None]
        Zbar_m_zhat[1] = lmd.rad_wrap_pi(Zbar_m_zhat[1])

        S_t = (Zbar_m_zhat * self.wght_c) @ Zbar_m_zhat.T


        chi_xmmu_bars = self.chi_x_bar - self.mu_bar[:,None]
        chi_xmmu_bars[2] = lmd.rad_wrap_pi(chi_xmmu_bars[2])

        self.sigma_x_z = (chi_xmmu_bars * self.wght_c) @ Zbar_m_zhat.T

        K_t = self.sigma_x_z @ sp.linalg.inv(S_t)

        # set_trace()
        # z_subtract = zz - z_hat[:,ii]
        z_subtract = zz.T[self.lm_idx] - z_hat
        z_subtract[1] = lmd.rad_wrap_pi(z_subtract[1])

        self.mu = self.mu_bar + (K_t @ z_subtract)
        self.mu[2] = lmd.rad_wrap_pi(self.mu[2])
        self.sigma = self.sigma_bar - K_t @ S_t @ K_t.T

        # p_zt *= np.det()

        self.K_hist.append(K_t)
    #

    # def calc_zz_ukf(self):
    def calc_zz_ukf(self, lm_ii):
        # xx_3x = np.array([self.xx]*self.num_lm).T

        # set_trace()

        r_vecs = lm_ii[:,None] - self.chi_x_bar[0:2]
        rngs = np.sqrt(np.sum(r_vecs**2,0))


        phis = np.arctan2(r_vecs[1], r_vecs[0]) - self.chi_x_bar[2]

        phis_wrapped = lmd.rad_wrap_pi(phis)

        self.zz_bar = np.array([rngs, phis_wrapped])
    #

    def loop_extra_landmarks(self, zz):
        # predict
        self.build_mu_sigma_a()

        self.generate_sig_points()

        self.chi_x_bar = self.chi_x

        self.calc_mu_sig_bars()
        # self.mu_bar = self.mu
        # self.sigma_bar = self.sigma

        # correct
        # set_trace()
        self.correction(zz)
        # self.correction(zz, self.mu, self.sigma)
    #

    # def calc_weights(self):
    #     wght_m_0 = self.l
    # #

#
