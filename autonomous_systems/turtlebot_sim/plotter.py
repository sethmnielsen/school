#!usr/env python3

import numpy as np
import params as pm
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

class Plotter():
    """ For animating turtlebot trajectory and estimation, and plotting the results"""

    def __init__(self):
        N = len(pm.t_arr)
        self.states = np.zeros((3, N))
        self.xhats = np.zeros((3, N))
        self.est_errors = np.zeros((3, N))
        self.error_covs = np.zeros((3, N))
        self.Chi = np.zeros((3,N))

        x0, y0, th0 = pm.state0
        self.states[:,0] = pm.state0
        self.xhats[:,0] = pm.state0

        # Robot physical constants    
        bot_radius = 0.5
        poly_res = 12
        bot_body_alpha = 0.4
        self.bot_body_heading = np.array([bot_radius, 0])

        # plt.ion()
        
        f1 = plt.figure(1)
        f1.clf()
        self.ax1:matplotlib.axes._axes.Axes = plt.axes()
                

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
        self.est_trail = plt.plot(self.xhats[:,0], self.xhats[:,1],'.', color=(1,0.65,0))

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

        sz = 10
        self.ax1.set_xlim(-sz, sz)
        self.ax1.set_ylim(-sz, sz)
        f1.canvas.draw()
        f1.show()

    def update_particles(self, state, xhat, Chi, covar, i):
        self.states[:, i] = state
        self.xhats[:, i] = xhat
        self.est_errors[:, i] = xhat - state
        self.error_covs[:, i] = covar
        
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
        # time.sleep(0.1)
        plt.pause(0.0001)
        

    def update_kalman(self, state, xhat, error_cov, i):
        self.states[i] = state
        self.xhats[i] = xhat
        self.est_errors[i] = xhat - state
        self.error_covs[i] = error_cov

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
        
        
    def make_plots(self):

        f2, axes2 = plt.subplots(3, 1, sharex=True)
        f2.suptitle('Three Landmarks UKF Localization - Estimation')
        axes2[0].plot(pm.t_arr, self.states[0], label='true')
        axes2[1].plot(pm.t_arr, self.states[1], label='true')
        axes2[2].plot(pm.t_arr, np.degrees(self.states[2]), label='true')

        axes2[0].plot(pm.t_arr, self.xhats[0], label='estimated')
        axes2[1].plot(pm.t_arr, self.xhats[1], label='estimated')
        axes2[2].plot(pm.t_arr, np.degrees(self.xhats[2]), label='estimated')

        axes2[0].set_ylabel('x position (m)')
        axes2[1].set_ylabel('y position (m)')
        axes2[2].set_ylabel('heading (deg)')
        axes2[2].set_xlabel('time (s)')
        
        axes2[0].legend()

        # ======================================

        f3, axes3 = plt.subplots(3, 1, sharex=True, num=3)
        f3.suptitle('Three Landmarks UKF Localization - Error')
        axes3[0].plot(pm.t_arr, self.est_errors[0], label='error')
        axes3[1].plot(pm.t_arr, self.est_errors[1])
        axes3[2].plot(pm.t_arr, self.est_errors[2])

        # Covariance plots (+/- 2 sigma)
        axes3[0].plot(pm.t_arr, 2*np.sqrt(self.error_covs[0]), linestyle='dashed', label='covariance', color='orange')
        axes3[1].plot(pm.t_arr, 2*np.sqrt(self.error_covs[1]), linestyle='dashed', color='orange')
        axes3[2].plot(pm.t_arr, 2*np.sqrt(self.error_covs[2]), linestyle='dashed', color='orange')

        axes3[0].plot(pm.t_arr, -2*np.sqrt(self.error_covs[0]), linestyle='dashed', color='orange')
        axes3[1].plot(pm.t_arr, -2*np.sqrt(self.error_covs[1]), linestyle='dashed', color='orange')
        axes3[2].plot(pm.t_arr, -2*np.sqrt(self.error_covs[2]), linestyle='dashed', color='orange')

        axes3[0].set_ylabel('x error (m)')
        axes3[1].set_ylabel('y error (m)')
        axes3[2].set_ylabel('heading error (deg)')
        axes3[2].set_xlabel('time (s)')
        
        axes3[0].legend()

        # plt.draw()
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