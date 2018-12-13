import numpy as np
import vtolParamHW10 as P
import sys
sys.path.append('..')  # add parent directory
import vtolParam as P0
from PIDControl import PIDControl

class vtolController:
    '''
        This class inherits other controllers in order to organize multiple controllers.
    '''

    def __init__(self):
        # Instantiates the SS_ctrl object
        self.hCtrl  = PIDControl(P.kp_h,  P.ki_h,  P.kd_h,   P.F_max, P.beta, P.Ts)
        self.thCtrl = PIDControl(P.kp_th, 0.0,     P.kd_th,  P.th_max, P.beta, P.Ts)
        self.zCtrl  = PIDControl(P.kp_z,  P.ki_z,  P.kd_z,   P.tau_max, P.beta, P.Ts)

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        h_r = y_r[1]

        z = y[0]
        h = y[1]
        th = y[2]

        F_tilde = self.hCtrl.PID(h_r, h, flag=False)
        Fe = P0.mt * P0.g
        F = Fe + F_tilde
        F = self.saturate(F, P.F_max)

        th_r = self.zCtrl.PID(z_r, z, flag=False)
        tau = self.thCtrl.PID(th_r, th, flag=False)
        tau = self.saturate(tau, P.tau_max)


        fr = F/2.0 + (1.0 / (2*P0.d)) * tau
        fl = F/2.0 - (1.0 / (2*P0.d)) * tau

        # print "********************"
        # print "z =", z
        # print "z_r =", z_r
        # print "th =", th*180/np.pi
        # print "th_r =", th_r*180/np.pi
        # print "tau =", tau

        return [fr, fl]

    def saturate(self, u, limit):
        if abs(u) > limit:
            u = limit*np.sign(u)
        return u
