from IPython.core.debugger import set_trace
from importlib import reload

import numpy as np
import scipy as sp
import scipy.signal

import matplotlib.pyplot as plt

class UUV():
    def __init__(self):
        self.mass = 100 # kg
        self.mass_inv = 1 / self.mass
        self.b_coeff = 20 # N*s/m

        self.F_nom = 50 # N

        self.x_noisy = np.zeros((2,1))

        self.dt = 0.05
        self.t0 = 0
        self.t1 = 5
        self.t2 = 25
        self.t3 = 30
        self.t4 = 50
        self.tt_t = np.array([self.t0, self.t1, self.t2, self.t3])

        # measurement covariance
        self.R_vel = 0
        self.R_pos = 0.001 # m^2
        # self.R_t = np.diag([self.R_vel, self.R_pos])
        self.R_t = self.R_pos

        # process noise, model uncertainty
        self.Q_vel = 0.01 # m^2/s^2
        self.Q_pos = 0.0001 # m^2
        self.Q_t = np.diag([self.Q_vel, self.Q_pos])

        # eq. of motion, state space matrices
        self.A_mat = np.array([[-self.b_coeff*self.mass_inv, 0], [1,0]])
        self.B_mat = np.array([[self.mass_inv], [0]])
        self.C_mat = np.array([0,1])
        self.D_mat = np.array([0])
        # set_trace()
        # discretize
        self.ss = sp.signal.StateSpace(self.A_mat, self.B_mat, self.C_mat, self.D_mat)
        # self.ss_dz = self.ss.sample(self.dt)
        self.ss_dz = self.ss.to_discrete(self.dt)
        self.A_dz = self.ss_dz.A
        self.B_dz = self.ss_dz.B
        self.C_dz = self.ss_dz.C
        self.D_dz = self.ss_dz.D

        # history lists
        self.tt_hist = []
        self.pos_tru = []
        self.vel_tru = []
        self.pos_est = []
        self.vel_est = []
        self.err_est_pos = []
        self.err_est_vel = []
        self.err_cov_pos = []
        self.err_cov_npos = []
        self.err_cov_vel = []
        self.err_cov_nvel = []
        self.K_gain_pos = []
        self.K_gain_vel = []

        # belief of correction
        self.mu_bar_t = None
        self.sigma_bar_t = None

        # belief of prediction
        self.mu_t = None
        self.sigma_t = None
        # initialize
        self.mu_tm1 = np.zeros((2,1))
        self.sigma_tm1 = np.eye(2)

        self.blah = 1
    #

    def kf_run(self):
        # start = int(self.t0)
        stop = int(self.t4 / self.dt)
        for ii in range(stop):
            self.tt = ii * self.dt
            if self.tt < self.t1:
                uu_t = self.F_nom
            elif self.t1 <= self.tt < self.t2:
                uu_t = 0
            elif self.t2 <= self.tt < self.t3:
                uu_t = -self.F_nom
            else:
                uu_t = 0
            #

            # ==============
            # ==============
            # ==============
            x_truth_A = np.dot(self.A_dz, self.x_noisy)
            x_truth_B = np.dot(self.B_dz, uu_t)
            x_truth = x_truth_A + x_truth_B
            # epsilon = np.sqrt(self.Q_t) @  np.random.randn(2,1)
            epsilon = np.random.multivariate_normal(np.array([0,0]),self.Q_t,1).T
            self.x_noisy = x_truth + epsilon

            # add noise to propagated state
            zz_t = self.x_noisy[1] + np.sqrt(self.R_pos) * np.random.randn(1)

            # ==============
            # ==============
            # ==============

            # prediction
            self.mu_bar_t = np.dot(self.A_dz, self.mu_tm1) + np.dot(self.B_dz, uu_t)

            sigtm1_AT = np.dot(self.sigma_tm1, self.A_dz.T)
            self.sigma_bar_t = np.dot(self.A_dz, sigtm1_AT) + self.Q_t


            # update Kalman gain
            # compute numerator
            sigb_CT = np.dot(self.sigma_bar_t, self.C_dz.T)
            # compute denominator
            C_sigb_CT = np.dot(self.C_dz, sigb_CT)
            C_sigb_CT_pR = C_sigb_CT + self.R_t
            # solve Kalman
            self.K_t = sp.linalg.solve(C_sigb_CT_pR.T, sigb_CT.T).T


            # correction
            z_C_mub = zz_t - np.dot(self.C_dz, self.mu_bar_t)
            self.mu_t = self.mu_bar_t + np.dot(self.K_t, z_C_mub)

            eye_K_C = np.eye(2) - np.dot(self.K_t, self.C_dz)
            self.sigma_t = np.dot(eye_K_C, self.sigma_bar_t)

            # ==============
            # ==============
            # ==============

            self.save_hist()

            self.mu_tm1 = self.mu_t
            self.sigma_tm1 = self.sigma_t
        #
    #

    def save_hist(self):
        self.tt_hist.append(self.tt)
        # set_trace()
        self.pos_tru.append(self.x_noisy[1,0]) # make sure this is a scalar
        self.vel_tru.append(self.x_noisy[0,0]) # make sure this is a scalar

        self.pos_est.append(self.mu_t[1,0])
        self.vel_est.append(self.mu_t[0,0])

        self.err_est_pos.append(self.x_noisy[1,0] - self.mu_t[1,0])
        self.err_est_vel.append(self.x_noisy[0,0] - self.mu_t[0,0])

        self.err_cov_pos.append(2*np.sqrt(self.sigma_t[1,1]))
        self.err_cov_npos.append(-2*np.sqrt(self.sigma_t[1,1]))

        self.err_cov_vel.append(2*np.sqrt(self.sigma_t[0,0]))
        self.err_cov_nvel.append(-2*np.sqrt(self.sigma_t[0,0]))

        self.K_gain_pos.append(self.K_t[1,0])
        self.K_gain_vel.append(self.K_t[0,0])
    #


    # def plot(self):
    #     f1 = plt.figure(1)
    #     ax1 = plt.axes()
    #
    #     pt1_1 = plt.plot(self.tt_hist, self.pos_tru)
    #     pt1_2 = plt.plot(self.tt_hist, self.vel_tru)
    #     pt1_3 = plt.plot(self.tt_hist, self.pos_est)
    #     pt1_4 = plt.plot(self.tt_hist, self.vel_est)
    #
    #     f1.show()
    #
    #     # ==================
    #
    #     f2 = plt.figure(2)
    #     ax2 = plt.axes()
    #
    #     pt2_1 = plt.plot(self.tt_hist, self.err_est_pos)
    #     pt2_2 = plt.plot(self.tt_hist, self.err_cov_pos)
    #
    #     f2.show()
    #
    #     # ==================
    #
    #     f3 = plt.figure(3)
    #     ax3 = plt.axes()
    #
    #     pt3_1 = plt.plot(self.tt_hist, self.err_est_vel)
    #     pt3_2 = plt.plot(self.tt_hist, self.err_cov_vel)
    #
    #     f3.show()
    #
    #     # ==================
    #
    #     f4 = plt.figure(4)
    #     ax4 = plt.axes()
    #
    #     pt4_1 = plt.plot(self.tt_hist, self.K_gain_pos)
    #
    #     f4.show()
    # #

#
