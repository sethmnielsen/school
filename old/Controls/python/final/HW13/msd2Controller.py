import numpy as np
import msd2ParamHW13 as P

class msd2Controller:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.x_hat = np.matrix([
            [0],
            [0],
            [0],
            [0]])
        self.F_d1 = 0.0          # control input, delayed by one sample
        self.integrator = 0.0    # integrator
        self.L = P.L             # observer gain
        self.A = P.A             # system model
        self.B = P.B
        self.C = P.C

        self.F_e = 0.0
        self.x3_dot = 0.0         # derivative of z
        self.x3_d1 = 0.0          # z delayed by 1 sample
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
        x3_r = y_r[0]
        x1 = y[0]
        x3 = y[2]

        m1 = P.m1
        m2 = P.m2
        k1 = P.k1
        k2 = P.k2
        b1 = P.b1
        b2 = P.b2

        self.updateObserver(y)
        x1_hat = self.x_hat[0]
        x3_hat = self.x_hat[2]

        # integrate error
        error = x3_r - x3
        self.integrateError(error)

        self.F_e = (-x1_hat*(-(b1*b2)/(m1*m2)) - x3_hat*(((b1/m1)*((b1/m1)+(b1/m2)+(b2/m2)))-(k1/m1)))*m1
        # self.F_e = 0

        F_tilde = -self.K*self.x_hat - self.ki*self.integrator

        # compute total force
        F = self.saturate(self.F_e + F_tilde)
        self.updateF(F)
        return [F.item(0)]

    def updateObserver(self, y_m):
        N = 10
        y = np.matrix([
            [y_m[0]],
            [y_m[2]]])
        for i in range(0, N):
            self.x_hat = self.x_hat + self.Ts/float(N)*(
                self.A*self.x_hat
                + self.B*(self.F_d1 - self.F_e)
                + self.L*(y-self.C*self.x_hat)
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
