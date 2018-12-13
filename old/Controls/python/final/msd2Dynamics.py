import numpy as np
import random
import msd2Param as P


class msd2Dynamics:
    '''
        Model the physical system
    '''

    def __init__(self):
        # Initial state conditions
        self.state = np.matrix([[P.x10],  # p1
                                [P.x20],  # p1dot
                                [P.x30],  # p2 - p1
                                [P.x40]]) # p2dot - p1dot
        #################################################
        # The parameters for any physical system are never known exactly.  Feedback
        # systems need to be designed to be robust to this uncertainty.  In the simulation
        # we model uncertainty by changing the physical parameters by a uniform random variable
        # that represents alpha*100 % of the parameter, i.e., alpha = 0.2, means that the parameter
        # may change by up to 20%.  A different parameter value is chosen every time the simulation
        # # is run.
        # alpha = 0.0  # Uncertainty parameter
        # self.m1 = P.m1 * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg
        # self.m2 = P.m2 * (1+2*alpha*np.random.rand()-alpha)  # Mass of the cart, kg
        # self.k1 = P.k1 * (1+2*alpha*np.random.rand()-alpha)  # Length of the rod, m
        # self.k2 = P.k2 * (1+2*alpha*np.random.rand()-alpha)  # Length of the rod, m
        # self.b1 = P.b1 * (1+2*alpha*np.random.rand()-alpha)  # Length of the rod, m
        # self.b2 = P.b2 * (1+2*alpha*np.random.rand()-alpha)  # Length of the rod, m

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
        m1 = P.m1
        m2 = P.m2
        k1 = P.k1
        k2 = P.k2
        b1 = P.b1
        b2 = P.b2

        x1  = state.item(0)
        x2  = state.item(1)
        x3  = state.item(2)
        x4  = state.item(3)

        F = u[0]

        # The equations of motion.
        x2d = x1*(-(b1*b2)/(m1*m2)) + x3*(((b1/m1)*((b1/m1)+(b1/m2)+(b2/m2)))-(k1/m1)) + x4*(-(b1/m1)) + F*(1.0/m1)
        x3d = x1*(b2/m2) + x3*(-((b1/m1)+(b1/m2)+(b2/m2))) + x4
        x4d = x1*(k2/m2) + x3*(-((k1/m1)+(k1/m2)+(k2/m2))) + F*(1.0/m1 + 1.0/m2)

        # build xdot and return
        xdot = np.matrix([[x2], [x2d], [x3d], [x4d]])
        return xdot

    def states(self):
        '''
            Returns all current states as a list
        '''
        return self.state.T.tolist()[0]
