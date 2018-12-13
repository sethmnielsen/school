import numpy as np
import msdParamHW13 as P

class msdController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.x_hat = np.matrix([
            [0.0],
            [0.0],
        ])
        self.u_d1 = 0.0          # control input, delayed by one sample
        self.integrator = 0.0    # integrator
        self.L = P.L             # observer gain
        self.A = P.A             # system model
        self.B = P.B
        self.C = P.C

        self.z_dot = 0.0         # derivative of z
        self.z_d1 = 0.0          # Angle z delayed by 1 sample
        self.integrator = 0.0    # integrator
        self.error_d1 = 0.0      # error signal delayed by 1 sample
        self.K = P.K             # state feedback gain
        self.ki = P.ki           # Input gain
        self.limit = P.F_max     # Maxiumum force
        self.beta = P.beta       # dirty derivative gain
        self.Ts = P.Ts           # sample rate of controller

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        z = y[0]

        self.updateObserver(y)
        z_hat = self.x_hat[0]

        # integrate error
        error = z_r - z
        self.integrateError(error)

        F_e = P.k * z_hat

        # Compute the state feedback controller
        F_tilde = -self.K*self.x_hat - self.ki*self.integrator

        # compute total force
        F = self.saturate(0 + F_tilde)
        self.updateU(F)

        return [F.item(0)]

    def updateObserver(self, y_m):
        # compute equilibrium force F_e
        z_hat = self.x_hat[0]
        F_e = P.k * z_hat

        N = 10
        for i in range(0, N):
            self.x_hat = self.x_hat + self.Ts/float(N)*(
                self.A*self.x_hat
                + self.B*(self.u_d1 - F_e)
                + self.L*(y_m-self.C*self.x_hat)
            )

    def updateU(self, u):
        self.u_d1 = u

    def integrateError(self, error):
        self.integrator = self.integrator + (self.Ts/2.0)*(error + self.error_d1)
        self.error_d1 = error

    def saturate(self,u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
