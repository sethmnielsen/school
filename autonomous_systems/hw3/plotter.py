#!usr/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from params import *

class Plotter():
    def __init__(self):
        self.states = []
        self.xhats = []
        self.est_errors = []
        self.error_covs = []
        self.t_arr = t_arr

        plt.ion()
        
        f1 = plt.figure(1)
        f1.clf()
        self.ax1 = plt.axes()

        head_x = np.array([0,curr_head[0]]) + x
        head_y = np.array([0,curr_head[1]]) + curr_y


        self.lmark0_pt = ptc.CirclePolygon((lmarks[0,0],lmarks[0,1]), radius=bot_radius, resolution=poly_res, alpha=bot_body_alpha, color='g')
        self.lmark1_pt = ptc.CirclePolygon((lmarks[1,0],lmarks[1,1]), radius=bot_radius, resolution=poly_res, alpha=bot_body_alpha, color='g')
        self.lmark2_pt = ptc.CirclePolygon((lmarks[2,0],lmarks[2,1]), radius=bot_radius, resolution=poly_res, alpha=bot_body_alpha, color='g')

        self.bot_body = ptc.CirclePolygon((curr_x, curr_y), radius=bot_radius, resolution=poly_res, alpha=bot_body_alpha, color='b')
        self.head0 = plt.plot(head_x, head_y, 'r')
        self.head1 = plt.plot(head_x, head_y)

        self.ax1.add_patch(self.bot_body)

        self.ax1.set_xlim(-sz, sz)
        self.ax1.set_ylim(-sz, sz)
        f1.canvas.draw()
        f1.show()

    def update(self, state, xhat, error_cov):
        x = state[0]
        y = state[1]
        theta = state[2]

        curr_head = heading2Rotation(theta) @ bot_body_heading

        head_x = np.array([0,curr_head[0]]) + x
        head_y = np.array([0,curr_head[1]]) + y

        self.bot_body.xy = (x, y)
        self.head0[0].set_xdata(head_x)
        self.head0[0].set_ydata(head_y)

        self.head1[0].set_xdata(states[:i,0])
        self.head1[0].set_ydata(states[:i,1])

        self.ax1.redraw_in_frame()
        # time.sleep(0.1)
        plt.pause(0.05)
        
        self.states.append(state)
        self.xhats.append(xhat)
        self.est_errors.append(xhat - state)
        self.error_covs.append(error_cov)

    def make_plots(self):

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

    def heading2Rotation(self, psi):
        c_psi = np.cos(psi)
        s_psi = np.sin(psi)

        R_yaw = np.array([[c_psi, s_psi],
                        [-s_psi, c_psi]])

        return R_yaw.T  # transpose to return body to inertial