from IPython.core.debugger import set_trace
from importlib import reload

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as ptc

import lmd
reload(lmd)


# ======================================
# ======================================

class TbotPlot():
    def __init__(self, tbot, est, est_err, sqrt_cov):


        f1 = plt.figure(1)
        f1.clf()
        ax1 = plt.axes()

        curr_x = tbot.xx_hist__np[0,0]
        curr_y = tbot.xx_hist__np[1,0]
        curr_psi = tbot.xx_hist__np[2,0]

        curr_head = tbot.r_b2i_hist[0] @ tbot.bot_body_heading

        head_x = [0,curr_head[0]] + curr_x
        head_y = [0,curr_head[1]] + curr_y

        # tbot
        pl0a = ptc.CirclePolygon((tbot.lm_1[0],tbot.lm_1[1]), radius=tbot.bot_body_radius, resolution=tbot.poly_res, alpha=tbot.bot_body_alpha, color='g')

        # lm 1
        pl1a = ptc.CirclePolygon((curr_x, curr_y), radius=tbot.bot_body_radius, resolution=tbot.poly_res, alpha=tbot.bot_body_alpha, color='b')

        # heading
        pl1b = plt.plot(head_x, head_y, 'r')
        # trail
        pl1ca = plt.plot(curr_x, curr_y, linewidth=8.0)
        # estimator trail
        pl1cb = plt.plot(est.mu_hist[0], est.mu_hist[1], '.', color=(1,0.65,0))

        # measurement vectors
        pl1da = plt.plot([curr_x,tbot.lm_1[0]],[curr_y,tbot.lm_1[1]], 'c')
        pl1d = plt.plot([curr_x,tbot.lm1_hist[0,0]],[curr_y,tbot.lm1_hist[1,0]], 'y')

        ax1.add_patch(pl1a)

        if tbot.num_lm > 1:

            pl0b = ptc.CirclePolygon((tbot.lm_2[0],tbot.lm_2[1]), radius=tbot.bot_body_radius, resolution=tbot.poly_res, alpha=tbot.bot_body_alpha, color='g')

            pl1ea = plt.plot([curr_x,tbot.lm_2[0]],[curr_y,tbot.lm_2[1]], 'c')
            pl1e = plt.plot([curr_x,tbot.lm2_hist[0,0]],[curr_y,tbot.lm2_hist[1,0]], 'y')

            ax1.add_patch(pl0b)
        #
        if tbot.num_lm > 2:

            pl0c = ptc.CirclePolygon((tbot.lm_3[0],tbot.lm_3[1]), radius=tbot.bot_body_radius, resolution=tbot.poly_res, alpha=tbot.bot_body_alpha, color='g')

            pl1fa = plt.plot([curr_x,tbot.lm_3[0]],[curr_y,tbot.lm_3[1]], 'c')
            pl1f = plt.plot([curr_x,tbot.lm3_hist[0,0]],[curr_y,tbot.lm3_hist[1,0]], 'y')

            ax1.add_patch(pl0c)
        #

        ax1.add_patch(pl0a)

        ax1.set_xlim(-tbot.field_sz,tbot.field_sz)
        ax1.set_ylim(-tbot.field_sz,tbot.field_sz)
        # ax1.legend()
        f1.show()
        # set_trace()
        #

        # def anim_field(self):

        for ii in range(tbot.num_t_pts):
            curr_x = tbot.xx_hist__np[0,ii]
            curr_y = tbot.xx_hist__np[1,ii]
            curr_psi = tbot.xx_hist__np[2,ii]

            curr_head = tbot.r_b2i_hist[ii] @ tbot.bot_body_heading

            head_x = [0,curr_head[0]] + curr_x
            head_y = [0,curr_head[1]] + curr_y

            # turtlebot: patch, and heading
            pl1a.xy = (curr_x, curr_y)
            pl1b[0].set_xdata(head_x)
            pl1b[0].set_ydata(head_y)

            # trail
            pl1ca[0].set_xdata(tbot.xx_hist__np[0,:ii])
            pl1ca[0].set_ydata(tbot.xx_hist__np[1,:ii])
            # estimate trail
            pl1cb[0].set_xdata(est.mu_hist[0,:ii])
            pl1cb[0].set_ydata(est.mu_hist[1,:ii])

            # measurement vectors
            pl1da[0].set_xdata([curr_x,tbot.lm_1[0]])
            pl1da[0].set_ydata([curr_y,tbot.lm_1[1]])
            pl1d[0].set_xdata([curr_x,tbot.lm1_hist[0,ii]])
            pl1d[0].set_ydata([curr_y,tbot.lm1_hist[1,ii]])

            if tbot.num_lm > 1:
                pl1ea[0].set_xdata([curr_x,tbot.lm_2[0]])
                pl1ea[0].set_ydata([curr_y,tbot.lm_2[1]])
                pl1e[0].set_xdata([curr_x,tbot.lm2_hist[0,ii]])
                pl1e[0].set_ydata([curr_y,tbot.lm2_hist[1,ii]])
            #
            if tbot.num_lm > 2:
                pl1fa[0].set_xdata([curr_x,tbot.lm_3[0]])
                pl1fa[0].set_ydata([curr_y,tbot.lm_3[1]])
                pl1f[0].set_xdata([curr_x,tbot.lm3_hist[0,ii]])
                pl1f[0].set_ydata([curr_y,tbot.lm3_hist[1,ii]])
            #

            ax1.redraw_in_frame()
            # time.sleep(0.1)
            plt.pause(0.005)
        #

        # ======================================

        f2 = plt.figure(2)
        f2.clf()
        ax2 = plt.axes()

        pl2a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='True: x')
        pl2b = plt.plot(tbot.t_span,est.mu_hist[0], label='Est: x')

        ax2.legend()
        f2.show()


        # ======================================

        f3 = plt.figure(3)
        f3.clf()
        ax3 = plt.axes()

        pl3a = plt.plot(tbot.t_span,tbot.xx_hist__np[1], label='True: y')
        pl3b = plt.plot(tbot.t_span,est.mu_hist[1], label='Est: y')

        ax3.legend()
        f3.show()


        # ======================================

        f4 = plt.figure(4)
        f4.clf()
        ax4 = plt.axes()

        pl4a = plt.plot(tbot.t_span,tbot.xx_hist__np[2], label='True: psi')
        pl4b = plt.plot(tbot.t_span,est.mu_hist[2], label='Est: psi')

        ax4.legend()
        f4.show()

        # ======================================
        # ======================================

        f5 = plt.figure(5)
        f5.clf()
        ax5 = plt.axes()

        pl5a = plt.plot(tbot.t_span,est_err[0], label='Err: x')
        pl5b = plt.plot(tbot.t_span,2*sqrt_cov[0], label='Cov: x')
        pl5c = plt.plot(tbot.t_span,-2*sqrt_cov[0], label='Cov: x')

        ax5.legend()
        f5.show()


        # ======================================

        f6 = plt.figure(6)
        f6.clf()
        ax6 = plt.axes()

        pl6a = plt.plot(tbot.t_span,est_err[1], label='Err: y')
        pl6b = plt.plot(tbot.t_span,2*sqrt_cov[1], label='Cov: y')
        pl6c = plt.plot(tbot.t_span,-2*sqrt_cov[1], label='Cov: y')

        ax6.legend()
        f6.show()


        # ======================================

        f7 = plt.figure(7)
        f7.clf()
        ax7 = plt.axes()

        pl7a = plt.plot(tbot.t_span,est_err[2], label='Err: psi')
        pl7b = plt.plot(tbot.t_span,2*sqrt_cov[2], label='Cov: psi')
        pl7c = plt.plot(tbot.t_span,-2*sqrt_cov[2], label='Cov: psi')

        ax7.legend()
        f7.show()


        # ======================================

        f8 = plt.figure(8)
        f8.clf()
        ax8 = plt.axes()

        pl8a = plt.plot(est.K_hist[:,0,0], label='K_gain: 0,0')
        pl8b = plt.plot(est.K_hist[:,0,1], label='K_gain: 0,1')
        pl8c = plt.plot(est.K_hist[:,1,0], label='K_gain: 1,0')
        pl8d = plt.plot(est.K_hist[:,1,1], label='K_gain: 1,1')
        pl8e = plt.plot(est.K_hist[:,2,0], label='K_gain: 2,0')
        pl8f = plt.plot(est.K_hist[:,2,1], label='K_gain: 2,1')

        ax8.legend()
        f8.show()
    #

#
