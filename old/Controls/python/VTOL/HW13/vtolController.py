import numpy as np
import vtolParamHW13 as P

class vtolController:
    # state feedback control using dirty derivatives to estimate zdot
    def __init__(self):
        self.x_hat_lon = np.matrix([
            [0],
            [0]])
        self.F_d1 = 0.0          # control input, delayed by one sample
        self.Llon = P.Llon             # observer gain
        self.Alon = P.Alon             # system model
        self.Blon = P.Blon
        self.Clon = P.Clon

        self.x_hat_lat = np.matrix([
            [0],
            [0],
            [0],
            [0]])
        self.tau_d1 = 0.0          # control input, delayed by one sample
        self.Llat = P.Llat             # observer gain
        self.Alat = P.Alat             # system model
        self.Blat = P.Blat
        self.Clat = P.Clat

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
        self.updateObserverLon(h)
        h_hat = self.x_hat_lon[0]
        self.updateObserverLat([z, theta])
        z_hat = self.x_hat_lat[0]

        # integrate error
        error_z = z_r - z
        self.integrateErrorZ(error_z)
        error_h = h_r - h
        self.integrateErrorH(error_h)

        # compute equilibrium force
        F_e = P.mt * P.g

        # Compute the state feedback controller
        F_tilde = -self.K_lon*self.x_hat_lon - self.ki_lon*self.integrator_h
        tau_unsat = -self.K_lat*self.x_hat_lat - self.ki_lat*self.integrator_z
        # print "ki_lon =", self.ki_lon
        # print "ki_lat =", self.ki_lat
        # print self.integrator_z
        # print tau_unsat.item(0)

        # compute total force
        F_unsat = F_e + F_tilde
        F = self.saturate_F(F_unsat)
        tau = self.saturate_tau(tau_unsat)

        self.updateF(F)
        self.updateTau(tau)

        self.integratorAntiWindup_lat(tau, tau_unsat)

        fr = F/2.0 + (1.0 / (2*P.d)) * tau
        fl = F/2.0 - (1.0 / (2*P.d)) * tau

        # print [fl.item(0), fr.item(0)]

        # fr = (F + tau)/2.0
        # fl = (F - tau)/2.0
        return [fr.item(0), fl.item(0)]

    def updateObserverLon(self, y_m):
        F_e = P.mt * P.g
        N = 10
        for i in range(0, N):
            self.x_hat_lon = self.x_hat_lon + self.Ts/float(N)*(
                self.Alon*self.x_hat_lon
                + self.Blon*(self.F_d1 - F_e)
                + self.Llon*(y_m-self.Clon*self.x_hat_lon)
            )

    def updateObserverLat(self, y_m):
        N = 10
        y = np.matrix([
            [y_m[0]],
            [y_m[1]]])
        for i in range(0, N):
            self.x_hat_lat = self.x_hat_lat + self.Ts/float(N)*(
                self.Alat*self.x_hat_lat
                + self.Blat*self.tau_d1
                + self.Llat*(y-self.Clat*self.x_hat_lat)
            )

    def updateF(self, F):
        self.F_d1 = F

    def updateTau(self, tau):
        self.tau_d1 = tau

    def integrateErrorH(self, error):
        self.integrator_h = self.integrator_h + (self.Ts/2.0)*(error + self.error_d1_h)
        self.error_d1_h = error

    def integrateErrorZ(self, error):
        self.integrator_z = self.integrator_z + (self.Ts/2.0)*(error + self.error_d1_z)
        self.error_d1_z = error

    def integratorAntiWindup_lat(self, u_sat, u_unsat):
         if abs(self.z_dot) < 0.01:
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
