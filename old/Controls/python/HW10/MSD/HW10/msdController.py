import numpy as np
import msdParamHW10 as P
import sys
sys.path.append('..')  # add parent directory
import msdParam as P0
from PIDControl import PIDControl


class msdController:

    def __init__(self):
        # Instantiates the PID object
        self.zCtrl = PIDControl(P.kp, P.ki, P.kd, P0.F_max, P.beta, P.Ts)
        self.limit = P0.F_max

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        z = y[0]

        print "z =", z

        # compute equilibrium Force Fe
        Fe = P0.k * z

        # compute the linearized torque using PID
        F_til = self.zCtrl.PID(z_r, z, True)

        print "Fe =",Fe
        print "F_til =",F_til

        # compute total torque
        F = Fe + F_til
        F = self.zCtrl.saturate(F)
        return [F]

    def saturate(self, u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
