import numpy as np
import dcParamHW11 as P

class dcController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.i_dot = 0.0         # derivative of z
        self.theta_dot = 0.0         # derivative of theta
        self.i_d1 = 0.0          # z delayed by 1 sample
        self.theta_d1 = 0.0          # Angle theta delayed by 1 sample
        self.K = P.K                 # state feedback gain
        self.kr = P.kr               # Input gain
        self.limit = P.V_max       # Maxiumum force
        self.beta = P.beta           # dirty derivative gain
        self.Ts = P.Ts               # sample rate of controller

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        th_r = y_r[0]
        theta = y[0]
        i = y[1]

        # print "th_r =", th_r * 180/np.pi
        # print "theta =", theta * 180/np.pi
        print "th_r =", th_r
        print "theta =", theta

        # differentiate z
        self.differentiateTheta(theta)
        self.differentiateI(i)

        # Construct the state
        x = np.matrix([[theta], [i], [self.theta_dot]])

        # compute equilibrium force
        V_e = P.R * i

        # Compute the state feedback controller
        V = -self.K*x + self.kr*th_r

        # compute total force
        V_sat = self.saturate(V + V_e)
        return [V_sat.item(0)]


    def differentiateTheta(self, theta):
        '''
            differentiate theta
        '''
        self.theta_dot = self.beta*self.theta_dot + (1-self.beta)*((theta - self.theta_d1) / self.Ts)
        self.theta_d1 = theta

    def differentiateI(self, i):
        '''
        differentiate i
        '''
        self.i_dot = self.beta*self.i_dot + (1-self.beta)*((i - self.i_d1) / self.Ts)
        self.i_d1 = i

    def saturate(self,u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u
