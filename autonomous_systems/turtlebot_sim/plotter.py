#!usr/env python3

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from utils import wrap
import seaborn as sns
from seaborn import xkcd_rgb as xcolor
sns.set_style("whitegrid")
sns.set_palette('deep',n_colors=100)

import hw6.params as pm

class Plotter():
    """ For animating turtlebot trajectory and estimation, and plotting the results"""

    def __init__(self, animate, params, particles=False):
        self.animate = animate
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
        bot_body_alpha = 0.7
        self.bot_body_heading = np.array([bot_radius, 0])

        if self.animate:
            f1 = plt.figure(1)
            self.ax1 = f1.add_subplot(1,1,1)  # type: Axes

            ##### ****TURTLEBOT**** #####
            self.trail, = self.ax1.plot(*pm.state0[:2], linewidth=2)  # trail
            self.est_trail, = self.ax1.plot(*pm.state0[:2],linewidth=2,color=(1,0.65,0))

            cur_head = self.heading2Rotation(th0) @ self.bot_body_heading                    
            head_x = np.array([0,cur_head[0]]) + x0    
            head_y = np.array([0,cur_head[1]]) + y0
            self.bot_body = ptc.CirclePolygon( (x0, y0), 
                                            radius=bot_radius, 
                                            resolution=poly_res, 
                                            alpha=bot_body_alpha, 
                                            color='b' )
            self.heading, = self.ax1.plot(head_x, head_y, 'r') # current heading
            self.ax1.add_patch(self.bot_body)
            

            ##### ****LANDMARKS**** #####
            # self.lmarks_line = []
            for i in range(pm.num_lms):
                lmark_patch = ptc.CirclePolygon( (pm.lmarks[0,i], pm.lmarks[1,i]),
                                            bot_radius/2, 
                                            poly_res, 
                                            alpha=bot_body_alpha, 
                                            color=xcolor['pale green'],
                                            ec=xcolor['dark pastel green'] )
                self.ax1.add_patch(lmark_patch)

                ##### ****COVARIANCE ELLIPSES**** #####                
                covar_patch = ptc.Ellipse( (pm.lmarks[0,i], pm.lmarks[1,i]),
                                            width=1, 
                                            height=1,
                                            angle=0, 
                                            alpha=0.2, 
                                            color='darkseagreen' )
                # self.ax1.add_patch(covar_patch)


            self.lmark_estimates, = self.ax1.plot(pm.lmarks[0], pm.lmarks[1], 
                                               'x',
                                               c=xcolor["pale red"])


            ##### PARTICLES #####
            if particles:
                self.particles, = self.ax1.plot(self.Chi[0], self.Chi[1], '*', color='m')  # type: Line2D
                
            sz = pm.sz
            self.ax1.set_xlim(-sz, sz)
            self.ax1.set_ylim(-sz, sz)
            f1.canvas.draw()
            plt.show(block=False)

    def update_kalman_plot(self, state, xhat, error_cov, i):
        self.states[i] = state
        self.xhats[i] = xhat
        self.est_errors[i] = xhat - state
        self.covariance[i] = error_cov

        x = state[0]
        y = state[1]
        theta = state[2]

        # turtlebot body patch
        self.bot_body.xy = (x, y)

        # heading indicator
        cur_head = self.heading2Rotation(theta) @ self.bot_body_heading
        head_x = np.array([0,cur_head[0]]) + x
        head_y = np.array([0,cur_head[1]]) + y
        self.heading.set_xdata(head_x)
        self.heading.set_ydata(head_y)

        # trails
        self.trail[0].set_xdata(self.states[:i,0])
        self.trail[0].set_ydata(self.states[:i,1])
        self.est_trail[0].set_xdata(self.xhats[:i,0])
        self.est_trail[0].set_ydata(self.xhats[:i,1])

        # measurement vectors
        for k in range(pm.num_lms):
            self.lmarks_line[k].set_xdata([x, pm.lmarks[0,k]])
            self.lmarks_line[k].set_ydata([y, pm.lmarks[1,k]])

        self.ax1.relim() 
        self.ax1.autoscale_view(True,True,True) 

        self.ax1.redraw_in_frame()
        # time.sleep(0.1)
        plt.pause(0.005)

    def update_ekfs_plot(self, state, xhat, error_cov, i):
        self.states[:,i] = state
        self.xhats[:,i] = xhat[:3]
        self.covariance[:,i] = error_cov

        x, y, theta = state

        cur_head = self.heading2Rotation(theta) @ self.bot_body_heading

        head_x = np.array([0,cur_head[0]]) + x
        head_y = np.array([0,cur_head[1]]) + y

        # turtlebot patch and heading
        self.bot_body.xy = (x, y)
        self.heading.set_xdata(head_x)
        self.heading.set_ydata(head_y)

        # trails
        j = i+1
        self.trail.set_data(*self.states[:2,:j])
        self.est_trail.set_data(*self.xhats[:2,:j])

        # landmark estimates
        # self.lmark_estimates.set_data

        self.ax1.redraw_in_frame()
        plt.pause(0.05)
        
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

    def make_plots_ekfs(self, t_arr, covar):
        states = self.states
        xhats = self.xhats
        covar[covar<0] = 0
        error_bounds = 2*np.sqrt(covar)
        
        est_errors = xhats - states
        est_errors[2] = wrap(est_errors[2])

        # ======================================
        
        f2, axes2 = plt.subplots(3, 1, sharex=True, num=2)
        f2.suptitle('True and Estimated States')
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

        f3, axes3 = plt.subplots(3, 1, sharex=True, num=3)
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