import numpy as np
import bobParamHW11 as P

class bobController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.z_dot = 0.0         # derivative of z
        self.theta_dot = 0.0         # derivative of theta
        self.z_d1 = 0.0          # z delayed by 1 sample
        self.theta_d1 = 0.0          # Angle theta delayed by 1 sample
        self.K = P.K                 # state feedback gain
        self.kr = P.kr               # Input gain
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
        self.differentiateZ(z)
        self.differentiateTheta(theta)

        # Construct the state
        x = np.matrix([[z], [theta], [self.z_dot], [self.theta_dot]])

        # compute equilibrium force
        F_e = P.g*(P.m1*z/P.l + P.m2/2.0)

        # Compute the state feedback controller
        F_tilde = -self.K*x + self.kr*z_r

        # compute total force
        F = self.saturate(F_e + F_tilde)
        return [F.item(0)]

    def differentiateZ(self, z):
        '''
            differentiate z
        '''
        self.z_dot = self.beta*self.z_dot + (1-self.beta)*((z - self.z_d1) / self.Ts)
        self.z_d1 = z

    def differentiateTheta(self, theta):
        '''
            differentiate theta
        '''
        self.theta_dot = self.beta*self.theta_dot + (1-self.beta)*((theta - self.theta_d1) / self.Ts)
        self.theta_d1 = theta

    def saturate(self,u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
