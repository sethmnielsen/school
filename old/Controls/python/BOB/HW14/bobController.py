import numpy as np
import bobParamHW14 as P

class bobController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.x_hat = np.matrix([
            [0],
            [0],
            [0],
            [0]])
        self.d_hat = 0.0             # estimate of the disturbance
        self.F_d1 = 0.0          # control input, delayed by one sample
        self.integrator = 0.0    # integrator
        self.L = P.L             # observer gain
        self.Ld = P.Ld               # gain for disturbance observer
        self.A = P.A             # system model
        self.B = P.B
        self.C = P.C

        self.z_dot = 0.0         # derivative of z
        self.theta_dot = 0.0         # derivative of theta
        self.z_d1 = 0.0          # z delayed by 1 sample
        self.theta_d1 = 0.0          # Angle theta delayed by 1 sample
        self.integrator = 0.0        # integrator
        self.error_d1 = 0.0          # error signal delayed by 1 sample
        self.K = P.K                 # state feedback gain
        self.ki = P.ki               # Input gain
        self.limit = P.F_max       # Maxiumum force
        self.beta = P.beta           # dirty derivative gain
        self.Ts = P.Ts               # sample rate of controller

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        z = y[0]
        theta = y[1]

        # differentiate z
        self.updateObserver(y)
        z_hat = self.x_hat[0]

        # integrate error
        error = z_r - z
        self.integrateError(error)

        # compute equilibrium force
        F_e = P.g*(P.m1*z_hat/P.l + P.m2/2.0)

        F_tilde = -self.K*self.x_hat - self.ki*self.integrator - self.d_hat

        # compute total force
        F = self.saturate(F_e + F_tilde)
        self.updateF(F)
        return [F.item(0)]

    def updateObserver(self, y_m):
        # compute equilibrium force F_e
        z_hat = self.x_hat[0]
        F_e = P.g*(P.m1*z_hat/P.l + P.m2/2.0)

        N = 10
        y = np.matrix([
            [y_m[0]],
            [y_m[1]]])
        for i in range(0, N):
            self.x_hat = self.x_hat + self.Ts/float(N)*(
                self.A*self.x_hat
                + self.B*(self.F_d1 - F_e)
                + self.L*(y-self.C*self.x_hat)
            )
            self.d_hat = self.d_hat + self.Ts/float(N)*(
                self.Ld*(y-self.C*self.x_hat)
            )

    def updateF(self, F):
        self.F_d1 = F

    def integrateError(self, error):
        self.integrator = self.integrator + (self.Ts/2.0)*(error + self.error_d1)
        self.error_d1 = error

    def saturate(self,u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
