import numpy as np
import random
import dcParam as P


class dcDynamics:
    '''
        Model the physical system
    '''

    def __init__(self):
        # Initial state conditions
        self.state = np.matrix([[P.th0],
                                [P.i0],
                                [P.thd0]])
        #################################################
        # The parameters for any physical system are never known exactly.  Feedback
        # systems need to be designed to be robust to this uncertainty.  In the simulation
        # we model uncertainty by changing the physical parameters by a uniform random variable
        # that represents alpha*100 % of the parameter, i.e., alpha = 0.2, means that the parameter
        # may change by up to 20%.  A different parameter value is chosen every time the simulation
        # is run.
        alpha = 0.0  # Uncertainty parameter
        self.J = P.J * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg
        self.b = P.b * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg
        self.k = P.k * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg
        self.R = P.R * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg
        self.L = P.L * (1+2*alpha*np.random.rand()-alpha)  # Mass of the pendulum, kg

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
        th   = state.item(0)
        i    = state.item(1)
        thd  = state.item(2)

        V = u[0]
        # The equations of motion.
        thdd = (-self.b*thd + self.k*i)/self.J
        idot = (V - self.k*thd - self.R*i)/self.L

        # build xdot and return
        xdot = np.matrix([[thd], [idot], [thdd]])
        return xdot

    def outputs(self):
        '''
            Returns the measured outputs as a list
            [z, theta] with added Gaussian noise
        '''
        # re-label states for readability
        th = self.state.item(0)
        i = self.state.item(1)
        # add Gaussian noise to outputs
        th_m = th + random.gauss(0, 0.00000001)
        i_m = i + random.gauss(0, 0.00000001)
        # return measured outputs
        return [th, i]

    def states(self):
        '''
            Returns all current states as a list
        '''
        return self.state.T.tolist()[0]
