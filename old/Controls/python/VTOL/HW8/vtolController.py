import vtolParamHW7 as P
import numpy as np
import sys
sys.path.append('..')  # add parent directory
import vtolParam as P0
from PDControl import PDControl

class vtolController:
    '''
        This class inherits other controllers in order to organize multiple controllers.
    '''

    def __init__(self):
        # Instantiates the SS_ctrl object
        self.hCtrl  = PDControl(P.kp_h, P.kd_h,   P.F_max, P.beta, P.Ts)
        self.thCtrl = PDControl(P.kp_th, P.kd_th, P.F_max, P.beta, P.Ts)
        self.zCtrl  = PDControl(P.kp_z, P.kd_z,   P.F_max, P.beta, P.Ts)

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        h_r = y_r[0]
        z_r = y_r[1]

        z = y[0]
        h = y[1]
        th = y[2]

        F_tilde = self.hCtrl.PD(h_r, h, flag=False)
        Fe = P.P.mt * P.P.g
        F = Fe + F_tilde

        th_r = self.zCtrl.PD(z_r, z, flag=False)
        tau = self.thCtrl.PD(th_r, th, flag=False)

        return [F, tau]
