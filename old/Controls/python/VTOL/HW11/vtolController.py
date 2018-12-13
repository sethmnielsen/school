import numpy as np
import vtolParamHW11 as P

class vtolController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.z_dot = 0.0         # derivative of z
        self.z_d1 = 0.0          # z delayed by 1 sample
        self.theta_dot = 0.0         # derivative of theta
        self.theta_d1 = 0.0          # Angle theta delayed by 1 sample
        self.h_dot = 0.0          # Angle theta delayed by 1 sample
        self.h_d1 = 0.0            # Angle theta delayed by 1 sample
        self.K_lon = P.K_lon       # state feedback gain
        self.K_lat = P.K_lat       # state feedback gain
        self.kr_lon = P.kr_lon      # Input gain
        self.kr_lat = P.kr_lat      # Input gain
        self.limit = P.F_max       # Maxiumum force
        self.beta = P.beta           # dirty derivative gain
        self.Ts = P.Ts               # sample rate of controller

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        h_r = y_r[1]

        z = y[0]
        h = y[1]
        theta = y[1]

        # differentiate z
        self.differentiateZ(z)
        self.differentiateH(h)
        self.differentiateTheta(theta)

        # Construct the state
        xlon = np.matrix([[h], [self.h_dot]])
        xlat = np.matrix([[z], [theta], [self.z_dot], [self.theta_dot]])

        # compute equilibrium force
        F_e = P.mt * P.g

        # Compute the state feedback controller
        F_tilde = -self.K_lon*xlon + self.kr_lon*h_r
        tau = -self.K_lat*xlat + self.kr_lat*z_r

        # compute total force
        F = self.saturate(F_e + F_tilde)

        fr = F/2.0 + (1.0 / (2*P.d)) * tau
        fl = F/2.0 - (1.0 / (2*P.d)) * tau
        return [fr.item(0), fl.item(0)]

    def differentiateZ(self, z):
        '''
            differentiate z
        '''
        self.z_dot = self.beta*self.z_dot + (1-self.beta)*((z - self.z_d1) / self.Ts)
        self.z_d1 = z

    def differentiateH(self, h):
        '''
            differentiate h
        '''
        self.h_dot = self.beta*self.h_dot + (1-self.beta)*((h - self.h_d1) / self.Ts)
        self.h_d1 = h

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
