from IPython.core.debugger import set_trace
from importlib import reload

import numpy as np
import scipy as sp

import lmd
reload(lmd)


class TurtleBot():
    def __init__(self):


        # Initial conditions
        self.x0 = -5
        self.y0 = -3
        self.psi0 = 90 * lmd.d2r
        self.xx0_perf = np.array([self.x0, self.y0, self.psi0])
        self.xx = self.xx0_perf

        self.x0_prime = 0
        self.y0_prime = 0
        self.psi0_prime = 0
        self.xx0_prime = np.array([self.x0_prime, self.y0_prime, self.psi0_prime])

        # velocity noise characteristics
        self.alpha1 = 0.1 * 1
        self.alpha2 = 0.01 * 1
        self.alpha3 = 0.01 * 1
        self.alpha4 = 0.1 * 1

        # land mark
        # set_trace()
        self.num_lm = 3
        self.lm_1 = np.array([6,4])
        self.lm_2 = np.array([-7,8])
        self.lm_3 = np.array([6,-4])
        self.lm_all = [self.lm_1,self.lm_2,self.lm_3]

        if self.num_lm == 1:
            self.lm_all = self.lm_all[0]
        else:
            self.lm_all = self.lm_all[0:self.num_lm]
        #
        # set_trace()
        self.lm_all = np.array(self.lm_all).T
        # self.lm_all = self.lm_all[0:self.num_lm].T
        # self.lm_all = self.lm_1

        self.my_zero = np.zeros((self.num_lm))

        # sensor noise for each landmark measurement
        self.sigma_r = 0.1 * 1 # m
        self.sigma_phi = 0.05 * 1 # rad

        # simulation time management
        self.dt = 0.1
        self.t_init = 0
        self.t_fin = 20
        self.t_span = np.arange(self.t_init, self.t_fin, self.dt)
        self.num_t_pts = len(self.t_span)

        # plotting params
        # max field size, +- field_sz (m)
        self.field_sz = 10
        self.poly_res = 12
        self.bot_body_radius = 0.5
        self.bot_body_heading = lmd.i_vec_2d * self.bot_body_radius
        self.bot_body_alpha = 0.4
        # self.bot_body = ptc.Circle((0,0),0.5,alpha=0.4,color='b')
        # self.dir_vec = lmd.i_vec

        # create the desired inputs to the systems
        self.vv_w = 0.2
        self.ww_w = 0.6
        # self.uu_des_hist = [[], []]
        self.calc_uu_des_hist()

        self.zz_hist__np = np.zeros((200,2,self.num_lm))
    #

    def calc_uu_des_hist(self):
        self.uu_des_hist__np = self.calc_uu_des(self.t_span)
        self.uu_des_hist = self.uu_des_hist__np.tolist()

    def calc_uu_des(self, tt):
        self.vel_des = (1 + 0.5 * np.cos(2*np.pi * self.vv_w*tt)) * 1
        self.omega_des = (-0.2 + 2 * np.cos(2*np.pi * self.ww_w*tt)) * 1

        uu_des = np.array([self.vel_des, self.omega_des])
        return uu_des
    #

    def run_dynamics_sim(self):
        self.xx_hist = [[], [], []]
        self.zz_hist = [[], []]
        for ii in range(self.num_t_pts):
            self.uu = self.uu_des_hist__np[:,ii]
            self.xx = self.propagate_motion_model(self.uu, self.xx)

            self.calc_zz()

            # save for later
            self.xx_hist[0].append(self.xx[0])
            self.xx_hist[1].append(self.xx[1])
            self.xx_hist[2].append(self.xx[2])

            # set_trace()
            self.zz_hist__np[ii] = self.zz
        #
        self.xx_hist__np = np.array(self.xx_hist)

        self.calc_r_i2b()
        # set_trace()
    #

    def calc_r_i2b(self):
        # this function, when called in batch, returns a history
        # of b2i rotations, after a transpose of the returned value
        self.r_b2i_hist = lmd.Rz_2d_I2B(self.xx_hist__np[2]).T
    #

    def propagate_motion_model(self, uu, xx, noise=1):
        # set_trace()
        v_hat = uu[0]

        v_hat += noise * np.sqrt(self.alpha1*uu[0]**2 * self.alpha2*uu[1]**2) * np.random.randn()

        omega_hat = uu[1]

        omega_hat += noise * np.sqrt(self.alpha3*uu[0]**2 + self.alpha4*uu[1]**2) * np.random.randn()

        # gamma_hat = np.sqrt(self.alpha5*self.vel**2 + self.alpha6*self.omega**2) * np.random.randn()

        # ======================================

        # v_omega_hat = np.array([v_hat, omagea_hat])

        v_over_omega_hats = v_hat / omega_hat

        omega_hat_dt = omega_hat * self.dt
        # gamma_hat_dt = gamma_hat * self.dt

        x_prime = xx[0] + v_over_omega_hats * ( -np.sin(xx[2]) + np.sin(xx[2] + omega_hat_dt) )

        y_prime = xx[1] + v_over_omega_hats * ( np.cos(xx[2]) - np.cos(xx[2] + omega_hat_dt) )

        psi_prime = lmd.rad_wrap_pi(xx[2] + omega_hat_dt) #+ gamma_hat_dt

        xx = np.array([x_prime, y_prime, psi_prime])
        return xx
    #

    def calc_zz(self):

        r_vecs = (self.lm_all.T - self.xx[0:2]).T
        rngs = np.sqrt(np.sum(r_vecs**2,0))
        rngs += self.sigma_r * np.random.randn(self.num_lm)

        phis = np.arctan2(r_vecs[1], r_vecs[0]) - self.xx[2]

        phis += self.sigma_phi * np.random.randn(self.num_lm)
        phis_wrapped = lmd.rad_wrap_pi(phis)

        # set_trace()

        self.zz = np.array([rngs, phis_wrapped])
    #

    def check_zz(self):

        my_zero = np.zeros((self.num_lm))
        # self.lm1_hist = []
        # self.lm2_hist = []
        # self.lm3_hist = []

        self.lm_hist_pre = [[] for ii in range(self.num_lm)]

        for ii in range(self.num_t_pts):
            # ======================
            # compute location of landmarks from zz
            curr_xy = self.xx_hist__np[0:2,ii]
            # set_trace()
            rng = np.asarray([self.zz_hist__np[ii,0,:],self.my_zero])
            psi = lmd.rad_wrap_pi(self.zz_hist__np[ii,1,:] + self.xx_hist__np[2,ii])

            r_b2is = lmd.Rz_2d_I2B(psi).T
            # new_rng = []
            # set_trace()
            for jj in range(self.num_lm):
                # new_rng.append(r_b2is[jj] @ rng[:,jj])
                self.lm_hist_pre[jj].append(curr_xy + (r_b2is[jj] @ rng[:,jj]))
            #
            # new_rng = np.asarray(new_rng).T
            #
            # self.lm1_hist.append(curr_xy + new_rng[:,0])
            # self.lm2_hist.append(curr_xy + new_rng[:,1])
            # self.lm3_hist.append(curr_xy + new_rng[:,2])
            # ======================
        #
        # set_trace()
        # self.lm1_hist = np.asarray(self.lm1_hist).T
        # self.lm2_hist = np.asarray(self.lm2_hist).T
        # self.lm3_hist = np.asarray(self.lm3_hist).T
        self.lm1_hist = np.asarray(self.lm_hist_pre[0]).T
        if self.num_lm > 1:
            self.lm2_hist = np.asarray(self.lm_hist_pre[1]).T
        #
        if self.num_lm > 2:
            self.lm3_hist = np.asarray(self.lm_hist_pre[2]).T
        #
#
