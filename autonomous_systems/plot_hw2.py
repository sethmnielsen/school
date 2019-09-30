import numpy as np
import matplotlib.pyplot as plt
from ekf_hw2 import EKF
import matplotlib.patches as ptc

def heading2Rotation(psi):
    c_psi = np.cos(psi)
    s_psi = np.sin(psi)

    R_yaw = np.array([[c_psi, s_psi],
                     [-s_psi, c_psi]])

    return R_yaw.T  # transpose to return body to inertial

if __name__ == '__main__':
    ekf = EKF()
    ekf.run()

    states = ekf.state_hist
    xhats = ekf.state_hist
    est_errors = ekf.est_error_hist
    error_covs = ekf.error_cov_hist
    t_span = ekf.t_arr

    # Constants    
    bot_radius = 0.5
    bot_body_heading = np.array([bot_radius, 0])
    poly_res = 12
    bot_body_alpha = 0.4

    plt.ion()
    
    f1 = plt.figure(1)
    f1.clf()
    ax1 = plt.axes()

    curr_x = states[0,0]
    curr_y = states[0,1]
    curr_psi = states[0,2]
    
    curr_head = heading2Rotation(curr_psi) @ bot_body_heading

    head_x = np.array([0,curr_head[0]]) + curr_x
    head_y = np.array([0,curr_head[1]]) + curr_y

    # set_trace()
    pl1a = ptc.CirclePolygon((curr_x, curr_y), radius=bot_radius, resolution=poly_res, alpha=bot_body_alpha, color='b')
    pl1b = plt.plot(head_x, head_y, 'r')
    pl1c = plt.plot(head_x, head_y)

    ax1.add_patch(pl1a)

    ax1.set_xlim(-ekf.sz, ekf.sz)
    ax1.set_ylim(-ekf.sz, ekf.sz)
    f1.canvas.draw()
    f1.show()

    for i in range(ekf.N-1):
        curr_x = states[i,0]
        curr_y = states[i,1]
        curr_psi = states[i,2]

        curr_head = heading2Rotation(curr_psi) @ bot_body_heading

        head_x = np.array([0,curr_head[0]]) + curr_x
        head_y = np.array([0,curr_head[1]]) + curr_y

        pl1a.xy = (curr_x, curr_y)
        pl1b[0].set_xdata(head_x)
        pl1b[0].set_ydata(head_y)

        pl1c[0].set_xdata(states[:i,0])
        pl1c[0].set_ydata(states[:i,1])

        ax1.redraw_in_frame()
        # time.sleep(0.1)
        plt.pause(0.05)
    #


    # ======================================

    f2 = plt.figure(2)
    f2.clf()
    ax2 = plt.axes()

    pl2a = plt.plot(t_span, states[:,0], label='True: x')
    pl2a = plt.plot(t_span, xhats[:,0], label='Est: x')

    ax2.legend()
    # f2.show()


    # ======================================

    f3 = plt.figure(3)
    f3.clf()
    ax3 = plt.axes()

    pl3a = plt.plot(t_span, states[:,1], label='True: y')
    pl3a = plt.plot(t_span,  xhats[:,1], label='Est: y')

    ax3.legend()
    # f3.show()


    # ======================================

    f4 = plt.figure(4)
    f4.clf()
    ax4 = plt.axes()

    pl4a = plt.plot(t_span,states[:,2], label='True: psi')
    pl4a = plt.plot(t_span, xhats[:,2], label='Est: psi')

    ax4.legend()
    # f4.show()

    # ======================================
    # ======================================

    f5 = plt.figure(5)
    f5.clf()
    ax5 = plt.axes()

    pl5a = plt.plot(t_span,est_errors[:,0], label='Err: x')
    pl5a = plt.plot(t_span,2*np.sqrt(error_covs[:,0]), label='Cov: x')
    pl5a = plt.plot(t_span,-2*np.sqrt(error_covs[:,0]), label='Cov: x')

    ax5.legend()
    # f5.show()


    # ======================================

    f6 = plt.figure(6)
    f6.clf()
    ax6 = plt.axes()

    pl6a = plt.plot(t_span,est_errors[:,1], label='Err: y')
    pl6a = plt.plot(t_span,2*np.sqrt(error_covs[:,1]), label='Cov: y')
    pl6a = plt.plot(t_span,-2*np.sqrt(error_covs[:,1]), label='Cov: y')

    ax6.legend()
    # f6.show()


    # ======================================

    f7 = plt.figure(7)
    f7.clf()
    ax7 = plt.axes()

    pl7a = plt.plot(t_span,est_errors[:,2], label='Err: psi')
    pl7a = plt.plot(t_span,2*np.sqrt(error_covs[:,2]), label='Cov: psi')
    pl7a = plt.plot(t_span,-2*np.sqrt(error_covs[:,2]), label='Cov: psi')

    ax7.legend()
    # f7.show()

    plt.show()

    print("Finished everything")