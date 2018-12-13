import numpy as np
import random
import bobParam as P


class bobDynamics:
    '''
        Model the physical system
    '''

    def __init__(self):
        # Initial state conditions
        self.state = np.matrix([[P.z0],          # z initial position
                                [P.th0],      # Theta initial orientation
                                [P.zd0],       # zdot initial velocity
                                [P.thd0]])  # Thetadot initial velocity
        #################################################
        # The parameters for any physical system are never known exactly.  Feedback
        # systems need to be designed to be robust to this uncertainty.  In the simulation
        # we model uncertainty by changing the physical parameters by a uniform random variable
        # that represents alpha*100 % of the parameter, i.e., alpha = 0.2, means that the parameter
        # may change by up to 20%.  A different parameter value is chosen every time the simulation
        # is run.
        alpha = 0.2  # Uncertainty parameter
        self.m1 = P.m1 * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg
        self.m2 = P.m2 * (1+2*alpha*np.random.rand()-alpha)  # Mass of the cart, kg
        self.l = P.ell * (1+2*alpha*np.random.rand()-alpha)  # Length of the rod, m
        # self.m1 = P.m1
        # self.m2 = 2
        self.r = P.radius
        self.g = P.g  # the gravity constant is well known and so we don't change it.

    def propagateDynamics(self, u):
        '''
            Integrate the differential equations defining dynamics
            P.Ts is the time step between function calls.
            u contains the system input(s).
        '''
        # Integrate ODE using Runge-Kutta RK4 algorithm
        k1 = self.derivatives(self.state, u)
        k2 = self.derivatives(self.state + P.Ts/2*k1, u)
        k3 = self.derivatives(self.state + P.Ts/2*k2, u)
        k4 = self.derivatives(self.state + P.Ts*k3, u)
        self.state += P.Ts/6 * (k1 + 2*k2 + 2*k3 + k4)

    def derivatives(self, state, u):
        '''
            Return xdot = f(x,u), the derivatives of the continuous states, as a matrix
        '''
        # re-label states and inputs for readability
        z   = state.item(0)
        th  = state.item(1)
        zd  = state.item(2)
        thd = state.item(3)

        F = u[0]
        # The equations of motion.
        M = np.matrix([[1.0, 0],
                       [0.0, self.m1*z**2 + (self.m2*self.l**2)/3.0]])
        C = np.matrix([[z*thd**2.0 - self.g*np.sin(th)],
                       [F*self.l*np.cos(th) - self.g*np.cos(th)*(self.m1*z + self.m2*self.l/2.0) - 2.0*self.m1*z*zd*thd]])
        tmp = np.linalg.inv(M)*C
        zdd = tmp.item(0)
        thdd = tmp.item(1)

        if z >= self.l and zd > 0 and zdd > 0:
            self.state[0] = self.l
            self.state[2] = 0
            zdd = 0
        elif z <= 0 and zd < 0 and zdd < 0:
            self.state[0] = 0
            self.state[2] = 0
            zdd = 0

        if th >= P.th_max and thd > 0 and thdd > 0:
            self.state[1] = P.th_max
            self.state[3] = 0
            thdd = 0
        elif th <= -P.th_max and thd < 0 and thdd < 0:
            self.state[1] = -P.th_max
            self.state[3] = 0
            thdd = 0

        # build xdot and return
        xdot = np.matrix([[zd], [thd], [zdd], [thdd]])
        return xdot

    def outputs(self):
        '''
            Returns the measured outputs as a list
            [z, theta] with added Gaussian noise
        '''
        # re-label states for readability
        z = self.state.item(0)
        theta = self.state.item(1)
        # add Gaussian noise to outputs
        z_m = z + random.gauss(0, 0.001)
        theta_m = theta + random.gauss(0, 0.001)
        # return measured outputs
        return [z, theta]

    def states(self):
        '''
            Returns all current states as a list
        '''
        return self.state.T.tolist()[0]
