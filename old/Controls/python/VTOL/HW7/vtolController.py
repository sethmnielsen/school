import vtolParamHW7 as P
import numpy as np
from PDControl import PDControl

class vtolController:
    '''
        This class inherits other controllers in order to organize multiple controllers.
    '''

    def __init__(self):
        # Instantiates the SS_ctrl object
        self.hCtrl = PDControl(P.kp_h, P.kd_h, P.F_max, P.beta, P.Ts)

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        h_r = y_r[0]
        h = y[1]
        # the force applied to the cart comes from the inner loop PD control
        F_tilde = self.hCtrl.PD(h_r, h, flag=False)
        Fe = P.P.mt * P.P.g
        F = Fe + F_tilde
        return [F]
