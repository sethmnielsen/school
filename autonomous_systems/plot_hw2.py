import numpy as np
import matplotlib.pyplot as plt
from ekf_hw2 import EKF

if __name__ == '__main__':
    ekf = EKF()
    ekf.run()
    
    f1 = plt.figure(1)
    f1.clf()
    ax1 = plt.axes()

    curr_x = tbot.xx_hist__np[0,0]
    curr_y = tbot.xx_hist__np[1,0]
    curr_psi = tbot.xx_hist__np[2,0]

    curr_head = tbot.r_b2i_hist[0] @ tbot.bot_body_heading

    head_x = [0,curr_head[0]] + curr_x
    head_y = [0,curr_head[1]] + curr_y

    # set_trace()
    pl1a = ptc.CirclePolygon((curr_x, curr_y), radius=tbot.bot_body_radius, resolution=tbot.poly_res, alpha=tbot.bot_body_alpha, color='b')
    pl1b = plt.plot(head_x, head_y, 'r')
    pl1c = plt.plot(head_x, head_y)

    ax1.add_patch(pl1a)

    ax1.set_xlim(-tbot.field_sz, tbot.field_sz)
    ax1.set_ylim(-tbot.field_sz, tbot.field_sz)
    # ax1.legend()
    f1.show()

    for ii in range(tbot.num_t_pts):
        curr_x = tbot.xx_hist__np[0,ii]
        curr_y = tbot.xx_hist__np[1,ii]
        curr_psi = tbot.xx_hist__np[2,ii]

        curr_head = tbot.r_b2i_hist[ii] @ tbot.bot_body_heading

        head_x = [0,curr_head[0]] + curr_x
        head_y = [0,curr_head[1]] + curr_y

        pl1a.xy = (curr_x, curr_y)
        pl1b[0].set_xdata(head_x)
        pl1b[0].set_ydata(head_y)

        pl1c[0].set_xdata(tbot.xx_hist__np[0,:ii])
        pl1c[0].set_ydata(tbot.xx_hist__np[1,:ii])

        ax1.redraw_in_frame()
        # time.sleep(0.1)
        plt.pause(0.005)
    #


    # ======================================

    f2 = plt.figure(2)
    f2.clf()
    ax2 = plt.axes()

    pl2a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='True: x')
    pl2a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='Est: x')

    ax2.legend()
    f2.show()


    # ======================================

    f3 = plt.figure(3)
    f3.clf()
    ax3 = plt.axes()

    pl3a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='True: y')
    pl3a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='Est: y')

    ax3.legend()
    f3.show()


    # ======================================

    f4 = plt.figure(4)
    f4.clf()
    ax4 = plt.axes()

    pl4a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='True: psi')
    pl4a = plt.plot(tbot.t_span,tbot.xx_hist__np[0], label='Est: psi')

    ax4.legend()
    f4.show()

    # ======================================
    # ======================================

    f5 = plt.figure(5)
    f5.clf()
    ax5 = plt.axes()

    pl5a = plt.plot(tbot.t_span,tbot.est_err[0], label='Err: x')
    pl5a = plt.plot(tbot.t_span,2*tbot.sqrt_cov[0], label='Cov: x')
    pl5a = plt.plot(tbot.t_span,-2*tbot.sqrt_cov[0], label='Cov: x')

    ax5.legend()
    f5.show()


    # ======================================

    f6 = plt.figure(6)
    f6.clf()
    ax6 = plt.axes()

    pl6a = plt.plot(tbot.t_span,tbot.est_err[1], label='Err: y')
    pl6a = plt.plot(tbot.t_span,2*tbot.sqrt_cov[1], label='Cov: y')
    pl6a = plt.plot(tbot.t_span,-2*tbot.sqrt_cov[1], label='Cov: y')

    ax6.legend()
    f6.show()


    # ======================================

    f7 = plt.figure(7)
    f7.clf()
    ax7 = plt.axes()

    pl7a = plt.plot(tbot.t_span,tbot.est_err[2], label='Err: psi')
    pl7a = plt.plot(tbot.t_span,2*tbot.sqrt_cov[2], label='Cov: psi')
    pl7a = plt.plot(tbot.t_span,-2*tbot.sqrt_cov[2], label='Cov: psi')

    ax7.legend()
    f7.show()
