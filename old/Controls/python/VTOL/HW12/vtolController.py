import numpy as np
import vtolParamHW12 as P

class vtolController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.z_dot = 0.0         # derivative of z
        self.z_d1 = 0.0          # z delayed by 1 sample
        self.theta_dot = 0.0         # derivative of theta
        self.theta_d1 = 0.0          # Angle theta delayed by 1 sample
        self.integrator_h = 0.0        # integrator
        self.integrator_z = 0.0        # integrator
        self.error_d1_h = 0.0          # error signal delayed by 1 sample
        self.error_d1_z = 0.0          # error signal delayed by 1 sample
        self.h_dot = 0.0          # Angle theta delayed by 1 sample
        self.h_d1 = 0.0            # Angle theta delayed by 1 sample
        self.K_lon = P.K_lon       # state feedback gain
        self.K_lat = P.K_lat       # state feedback gain
        self.ki_lon = P.ki_lon      # Input gain
        self.ki_lat = P.ki_lat      # Input gain
        self.limit_F = P.F_max       # Maxiumum force
        self.limit_tau = P.tau_max
        self.beta = P.beta           # dirty derivative gain
        self.Ts = P.Ts               # sample rate of controller

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        z_r = y_r[0]
        h_r = y_r[1]

        z = y[0]
        h = y[1]
        theta = y[2]

        # differentiate z
        self.differentiateZ(z)
        self.differentiateH(h)
        self.differentiateTheta(theta)

        # integrate error
        error_z = z_r - z
        self.integrateErrorZ(error_z)
        error_h = h_r - h
        self.integrateErrorH(error_h)

        # Construct the state
        xlon = np.matrix([[h], [self.h_dot]])
        xlat = np.matrix([[z], [theta], [self.z_dot], [self.theta_dot]])

        # compute equilibrium force
        F_e = P.mt * P.g

        # Compute the state feedback controller
        F_tilde = -self.K_lon*xlon - self.ki_lon*self.integrator_h
        tau_unsat = -self.K_lat*xlat - self.ki_lat*self.integrator_z

        # compute total force
        F_unsat = F_e + F_tilde
        F = self.saturate_F(F_unsat)
        tau = self.saturate_tau(tau_unsat)

        # self.integratorAntiWindup_lon(F, F_unsat)
        self.integratorAntiWindup_lat(tau, tau_unsat)

        fr = F/2.0 + (1.0 / (2*P.d)) * tau
        fl = F/2.0 - (1.0 / (2*P.d)) * tau

        # fr = (F + tau)/2.0
        # fl = (F - tau)/2.0
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

    def integrateErrorH(self, error):
        self.integrator_h = self.integrator_h + (self.Ts/2.0)*(error + self.error_d1_h)
        self.error_d1_h = error

    def integrateErrorZ(self, error):
        self.integrator_z = self.integrator_z + (self.Ts/2.0)*(error + self.error_d1_z)
        self.error_d1_z = error

    def integratorAntiWindup_lon(self, u_sat, u_unsat):
         # integrator anti - windup
         if abs(self.h_dot) > 0.01:
             if self.ki_lon != 0.0:
                self.integrator_h = self.integrator_h + self.Ts/self.ki_lon*(u_sat-u_unsat);

    def integratorAntiWindup_lat(self, u_sat, u_unsat):
         if abs(self.z_dot) > 0.01:
             if self.ki_lat != 0.0:
                self.integrator_z = self.integrator_z + self.Ts/self.ki_lat*(u_sat-u_unsat);

    def saturate_F(self,u):
        if abs(u) > self.limit_F:
            u = self.limit_F*np.sign(u)
        return u

    def saturate_tau(self,u):
        if abs(u) > self.limit_tau:
            u = self.limit_tau*np.sign(u)
        return u
