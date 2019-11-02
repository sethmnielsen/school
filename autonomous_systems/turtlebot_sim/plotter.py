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

class Plotter():
    """ For animating turtlebot trajectory and estimation, and plotting the results"""

    def __init__(self, animate, params):
        self.animate = animate
        pm = params
        N = pm.N
        self.states = np.zeros((3, N))
        self.xhats = np.zeros((3, N))
        self.est_errors = np.zeros((3, N))
        self.covariance = np.zeros((3, N))
        self.Chi = np.zeros((3,N))
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
            # self.particles = plt.plot(self.Chi[0], self.Chi[1], '*', color='m')  # type: Line2D

            # Draw landmarks
            # self.lmarks_line = []
            for i in range(pm.num_lms):
                patch = ptc.CirclePolygon( (pm.lmarks[0,i], pm.lmarks[1,i]),
                                            bot_radius, 
                                            poly_res, 
                                            alpha=bot_body_alpha, 
                                            color='g' )
                self.ax1.add_patch(patch)
                

                # measurement vectors
                # line = plt.plot([x0, pm.lmarks[0,i]], [y0, pm.lmarks[1,i]], 'c')
                # self.lmarks_line.append(line[0])

            self.ax1.add_patch(self.bot_body)

            sz = pm.sz
            self.ax1.set_xlim(-sz, sz)
            self.ax1.set_ylim(-sz, sz)
            f1.canvas.draw()
            f1.show()

    def init_eif_plots(self):
        f2 = plt.figure(2)
        f2.clf()
        self.ax2 = f2.add_subplot(1,1,1)  # type: Axes

        self.trail = plt.plot(pm.x0, pm.y0, linewidth=8.0)  # trail
        self.est_trail = plt.plot(self.xhats[0], self.xhats[1],'.', color=(1,0.65,0))
        f2.canvas.draw()
        f2.show()
            
    def update_kalman_plot(self, state, xhat, error_cov, i):
        self.states[i] = state
        self.xhats[i] = xhat
        self.est_errors[i] = xhat - state
        self.covariance[i] = error_cov

        x = state[0]
        y = state[1]
        theta = state[2]

        cur_head = self.heading2Rotation(theta) @ self.bot_body_heading

        head_x = np.array([0,cur_head[0]]) + x
        head_y = np.array([0,cur_head[1]]) + y

        # turtlebot patch and heading
        self.bot_body.xy = (x, y)
        self.heading[0].set_xdata(head_x)
        self.heading[0].set_ydata(head_y)
        # trails
        self.trail[0].set_xdata(self.states[:i,0])
        self.trail[0].set_ydata(self.states[:i,1])
        self.est_trail[0].set_xdata(self.xhats[:i,0])
        self.est_trail[0].set_ydata(self.xhats[:i,1])

        # measurement vectors
        for k in range(pm.num_lms):
            self.lmarks_line[k].set_xdata([x, pm.lmarks[0,k]])
            self.lmarks_line[k].set_ydata([y, pm.lmarks[1,k]])

        self.ax1.redraw_in_frame()
        # time.sleep(0.1)
        plt.pause(0.005)
        
    def update_mcl_plot(self, state, xhat, Chi, covar, i):
        self.states[:, i] = state
        self.xhats[:, i] = xhat
        self.est_errors[:, i] = xhat - state
        self.covariance[:, i] = covar

        if self.animate:        
            cur_state = state
            x = cur_state[0]
            y = cur_state[1]
            theta = cur_state[2]

            cur_head = self.heading2Rotation(theta) @ self.bot_body_heading

            head_x = np.array([0,cur_head[0]]) + x
            head_y = np.array([0,cur_head[1]]) + y

            # turtlebot patch and heading
            self.bot_body.xy = (x, y)
            self.heading[0].set_xdata(head_x)
            self.heading[0].set_ydata(head_y)
            # trails
            self.trail[0].set_xdata(self.states[0,:i])
            self.trail[0].set_ydata(self.states[1,:i])
            self.est_trail[0].set_xdata(self.xhats[0,:i])
            self.est_trail[0].set_ydata(self.xhats[1,:i])
            # particles
            self.particles[0].set_xdata(Chi[0])
            self.particles[0].set_ydata(Chi[1])
            
            # measurement vectors
            # for k in range(pm.num_lms):
            #     self.lmarks_line[k].set_xdata([x, pm.lmarks[0,k]])
            #     self.lmarks_line[k].set_ydata([y, pm.lmarks[1,k]])

            self.ax1.redraw_in_frame()
            plt.pause(0.0001)
        
    def update_eif_plot(self, state, xhat, i):
        self.states[:, i] = state
        self.xhats[:, i] = xhat

        if self.animate:        
            cur_state = state
            x = cur_state[0]
            y = cur_state[1]
            theta = cur_state[2]

            cur_head = self.heading2Rotation(theta) @ self.bot_body_heading

            head_x = np.array([0,cur_head[0]]) + x
            head_y = np.array([0,cur_head[1]]) + y

            # turtlebot patch and heading
            self.bot_body.xy = (x, y)
            self.heading[0].set_xdata(head_x)
            self.heading[0].set_ydata(head_y)
            # trails
            self.trail[0].set_xdata(self.states[0,:i])
            self.trail[0].set_ydata(self.states[1,:i])
            self.est_trail[0].set_xdata(self.xhats[0,:i])
            self.est_trail[0].set_ydata(self.xhats[1,:i])
            
            # measurement vectors
            # for k in range(pm.num_lms):
            #     self.lmarks_line[k].set_xdata([x, pm.lmarks[0,k]])
            #     self.lmarks_line[k].set_ydata([y, pm.lmarks[1,k]])

            self.ax1.redraw_in_frame()
            plt.pause(0.0001)
    
        
    def make_plots(self):
        a = 2
        b = 200
        t_arr = pm.t_arr[a:b]
        states = self.states[:, a:b]
        xhats = self.xhats[:, a:b]
        est_errors = self.est_errors[:, a:b]
        covar = self.covariance[:, a:b]
        error_bounds = 2*np.sqrt(covar)

        f2, axes2 = plt.subplots(3, 1, sharex=True, num=2)
        f2.suptitle('Three Landmarks MCL Localization - Estimation')
        axes2[0].plot(t_arr, states[0], label='true')
        axes2[1].plot(t_arr, states[1], label='true')
        axes2[2].plot(t_arr, states[2], label='true')

        axes2[0].plot(t_arr, xhats[0], label='estimated')
        axes2[1].plot(t_arr, xhats[1], label='estimated')
        axes2[2].plot(t_arr, xhats[2], label='estimated')

        axes2[0].set_ylabel('x position (m)')
        axes2[1].set_ylabel('y position (m)')
        axes2[2].set_ylabel('heading (deg)')
        axes2[2].set_xlabel('time (s)')
        
        axes2[0].legend()

        # ======================================

        f3, axes3 = plt.subplots(3, 1, sharex=True, num=3)
        f3.suptitle('Three Landmarks MCL Localization - Error')
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
        axes3[2].set_ylabel('heading error (deg)')
        axes3[2].set_xlabel('time (s)')
        
        axes3[0].legend()

        plt.draw()
        # plt.waitforbuttonpress(0)
        # plt.close('all')
        plt.show()

        print("Finished everything")

    def make_plots_eif(self, t_arr, ksi_hist, covar):
        states = self.states
        xhats = self.xhats
        est_errors = wrap(xhats - states, 2)
        covar[covar<0] = 0
        error_bounds = 2*np.sqrt(covar)

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