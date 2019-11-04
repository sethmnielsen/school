#!usr/env python3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from utils import wrap
import seaborn
seaborn.set_style("whitegrid")

pm = None

class PlotterMidterm():
    """ For animating turtlebot trajectory and estimation, and plotting the results"""

    def __init__(self, animate, params):
        self.animate = animate
        pm = params
        N = pm.N
        self.states = np.zeros((3, N))
        self.xhats = np.zeros((3, N))
        self.est_errors = np.zeros((3, N))
        self.covariance = np.zeros((3, N))
        self.ksi = np.zeros((3, N))

        x0, y0, th0 = pm.state0
        self.states[:,0] = pm.state0
        self.xhats[:,0] = pm.state0

        # Robot physical constants    
        bot_radius = 0.5
        poly_res = 12
        bot_body_alpha = 0.4
        self.bot_body_heading = np.array([bot_radius, 0])

        # plt.ion()
        if self.animate:
            f1 = plt.figure(1)
            f1.clf()
            self.ax1 = f1.add_subplot(1,1,1)  # type: Axes
                    

            # Draw turtlebot
            cur_head = self.heading2Rotation(th0) @ self.bot_body_heading                    
            head_x = np.array([0,cur_head[0]]) + x0    
            head_y = np.array([0,cur_head[1]]) + y0
            self.bot_body = ptc.CirclePolygon( (x0, y0), 
                                            radius=bot_radius, 
                                            resolution=poly_res, 
                                            alpha=bot_body_alpha, 
                                            color='b' )
            self.heading = plt.plot(head_x, head_y, 'r') # current heading
            self.trail = plt.plot(x0, y0, linewidth=8.0)  # trail
            self.est_trail = plt.plot(self.xhats[0], self.xhats[1],'.', color=(1,0.65,0))

            # Draw landmarks
            # self.lmarks_line = []
            for i in range(pm.num_lms):
                patch = ptc.CirclePolygon( (pm.lmarks[0,i], pm.lmarks[1,i]),
                                            bot_radius, 
                                            poly_res, 
                                            alpha=bot_body_alpha, 
                                            color='g' )
                self.ax1.add_patch(patch)
                

            self.ax1.add_patch(self.bot_body)

            sz = pm.sz
            self.ax1.set_xlim(-sz, sz)
            self.ax1.set_ylim(-sz, sz)
            f1.canvas.draw()
            f1.show()

    def update_eif_plot(self, state, xhat, i):
        self.states[:, i] = state
        self.xhats[:, i] = xhat

        if self.animate:        
            cur_state = state
            x = cur_state[0]
            y = cur_state[1]
            theta = cur_state[2]

            # trails
            self.trail[0].set_xdata(self.states[0,:i])
            self.trail[0].set_ydata(self.states[1,:i])
            self.est_trail[0].set_xdata(self.xhats[0,:i])
            self.est_trail[0].set_ydata(self.xhats[1,:i])

            # turtlebot patch and heading
            cur_head = self.heading2Rotation(theta) @ self.bot_body_heading

            head_x = np.array([0,cur_head[0]]) + x
            head_y = np.array([0,cur_head[1]]) + y

            self.bot_body.xy = (x, y)
            self.heading[0].set_xdata(head_x)
            self.heading[0].set_ydata(head_y)
            
            self.ax1.redraw_in_frame()
            plt.pause(0.0001)
    
        
    def make_plots_eif(self, t_arr, ksi_hist, covar):
        states = self.states
        xhats = self.xhats
        covar[covar<0] = 0
        error_bounds = 2*np.sqrt(covar)
        
        est_errors_nowrap = xhats - states
        est_errors = wrap(est_errors_nowrap, 2)

        # fat_errors = abs(est_errors_nowrap[2])>=np.pi
        # xhats[2][fat_errors] -= est_errors[2][fat_errors]
        # xhats[2][fat_errors] *= -1

        f12, axes12 = plt.subplots(3, 1, sharex=True, num=2)
        f12.suptitle('Information Vector vs Time')
        axes12[0].plot(t_arr, ksi_hist[0], 'b')
        axes12[1].plot(t_arr, ksi_hist[1], 'g')
        axes12[2].plot(t_arr, ksi_hist[2], 'r')

        axes12[0].set_ylabel('x position (m)')
        axes12[1].set_ylabel('y position (m)')
        axes12[2].set_ylabel('heading (rad)')
        axes12[2].set_xlabel('time (s)')

        # ======================================
        
        f2, axes2 = plt.subplots(3, 1, sharex=True, num=3)
        f2.suptitle('EIF True and Estimated States')
        axes2[0].plot(t_arr, states[0], label='true')
        axes2[1].plot(t_arr, states[1])
        axes2[2].plot(t_arr, states[2])

        axes2[0].plot(t_arr, xhats[0], label='estimated')
        axes2[1].plot(t_arr, xhats[1])
        axes2[2].plot(t_arr, xhats[2])

        axes2[0].set_ylabel('x position (m)')
        axes2[1].set_ylabel('y position (m)')
        axes2[2].set_ylabel('heading (rad)')
        axes2[2].set_xlabel('time (s)')
        
        axes2[0].legend()

        # ======================================

        f3, axes3 = plt.subplots(3, 1, sharex=True, num=4)
        f3.suptitle(r'Estimation Error and $2\sigma$ Bounds')
        axes3[0].plot(t_arr, est_errors[0], label='error')
        axes3[1].plot(t_arr, est_errors[1])
        axes3[2].plot(t_arr, est_errors[2])

        # Covariance plots (+/- 2 sigma)
        axes3[0].plot(t_arr,  error_bounds[0], linestyle='dashed', label='covariance', color='orange')
        axes3[1].plot(t_arr,  error_bounds[1], linestyle='dashed', color='orange')
        axes3[2].plot(t_arr,  error_bounds[2], linestyle='dashed', color='orange')

        axes3[0].plot(t_arr,  -error_bounds[0], linestyle='dashed', color='orange')
        axes3[1].plot(t_arr,  -error_bounds[1], linestyle='dashed', color='orange')
        axes3[2].plot(t_arr,  -error_bounds[2], linestyle='dashed', color='orange')

        axes3[0].set_ylabel('x error (m)')
        axes3[1].set_ylabel('y error (m)')
        axes3[2].set_ylabel('heading error (rad)')
        axes3[2].set_xlabel('time (s)')
        
        axes3[0].legend()

        plt.draw()
        # plt.waitforbuttonpress(0)
        # plt.close('all')
        plt.show()

        print("Finished everything")


    def heading2Rotation(self, psi):
        c_psi = np.cos(psi)
        s_psi = np.sin(psi)

        R_yaw = np.array([[c_psi, s_psi],
                        [-s_psi, c_psi]])

        return R_yaw.T  # transpose to return body to inertial