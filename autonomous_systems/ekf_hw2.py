import numpy as np
from numpy.linalg import multi_dot, inv, det
import scipy.signal as ss
import matplotlib.pyplot as plt
from angle import Angle


class EKF():
    
    def __init__(self):
        self.l = 20
        x = -5
        y = -3
        th = Angle(np.pi/2)
        self.x_state = np.array([x, y, th], dtype=object) # x, y, theta
        self.xhat = np.array([x, y, th], dtype=object)
        self.xbar = np.zeros(3)

        # time
        self.dt = 0.1
        t_end = 20
        self.t_arr = np.arange(0, t_end, self.dt)
        self.N = int(t_end / self.dt)

        self.v_c = 1 + 0.5*np.cos(2*np.pi*(0.2)*self.t_arr)
        self.omg_c = -0.2 + 2*np.cos(2*np.pi*(0.6)*self.t_arr)

        self.marks = np.array([[6, 4],
                            [-7, 8],
                            [6, -4]]).T

        self.z = np.zeros((3,2))
        
        # Noise
        self.alpha = np.array([0.1, 0.01, 0.01, 0.1])
        std_r = 0.1     # std dev of range
        std_phi = 0.05  # std dev of bearing

        self.K = np.zeros(3)
        self.R = np.diag([std_r**2, std_phi**2])
        self.P = np.eye(3)
        self.Pbar = np.eye(3)

        # history
        

    def run(self):
        for i in range(1, self.N-1):
            self.propagate_truth(self.v_c[i], self.omg_c[i], self.x_state)
            self.prediction_step(self.v_c[i], self.omg_c[i], self.xhat)
            self.measurement_correction()

    def propagate_truth(self, v, omg, state):
        sample_v = self.alpha[0] * v**2 + self.alpha[1] * omg**2
        sample_omg = self.alpha[2] * v**2 + self.alpha[3] * omg**2
        vhat = v + np.sqrt(sample_v)*np.random.randn()
        omghat = omg + np.sqrt(sample_omg)*np.random.randn()

        vo = vhat/omghat
        x = state[0]
        y = state[1]
        th = state[2]
        th_plus = th + omghat*self.dt
        x -= vo*np.sin(th.angle) + vo*np.sin(th_plus.angle)
        y += vo*np.cos(th.angle) + vo*np.cos(th_plus.angle)
        th = Angle(th_plus)
        state = np.array([x, y, th])

        mdx = self.marks[0] - x
        mdy = self.marks[1] - y
        r = np.sqrt(np.add(mdx**2,mdy**2)) * np.random.randn(3)
        phi_raw = np.arctan2(mdy, mdx) - th
        phi = np.array(phi_raw) * np.random.randn(3)

        self.z = np.array([r, phi]).T

    def prediction_step(self, v, omg, xhat):
        G = np.eye(3)        # Jacobian of g(u_t, x_t-1) wrt state
        V = np.zeros((3,2))  # Jacobian of g(u_t, x_t-1) wrt inputs
        M = np.zeros((2,2))  # noise in control space

        # convenience terms
        th = xhat[2]
        th_plus = th + omg*self.dt
        vo = v/omg
        c = np.cos(th.angle) - np.cos(th_plus.angle)
        s = np.sin(th.angle) - np.sin(th_plus.angle)

        # G matrix
        g02 = -vo * c
        g12 = -vo * s
        G[:2, 2] = [g02, g12]

        # V matrix
        v00 = -s / omg
        v10 =  c / omg  
        v01 =  v*s / omg**2  +  v*np.cos(th_plus.angle)*self.dt / omg
        v11 = -v*c / omg**2  +  v*np.sin(th_plus.angle)*self.dt / omg
        V = np.array([[v00, v01],
                      [v10, v11],
                      [  0, self.dt]])

        # M matrix
        a1, a2, a3, a4 = self.alpha
        M = np.diag([a1*v**2 + a2*omg**2, a3*v**2 + a4*omg**2])

        # Prediction state and covariance
        self.xbar = xhat + [-vo*s, vo*c, omg*self.dt]
        self.Pbar = multi_dot([G, self.P, G.T]) + multi_dot([V, M, V.T])

    def measurement_correction(self):
        for i in range(3):
            mdx = self.marks[0,i] - self.xbar[0]
            mdy = self.marks[1,i] - self.xbar[1]
            th = self.xbar[2]
            q = mdx**2 + mdy**2
            r = np.sqrt(q)
            phi = np.arctan2(mdy, mdx) - th
            zhat = np.array([r, phi.angle])
            H = np.array([[-mdx/r, -mdy/r,  0],
                          [ mdy/q, -mdx/q, -1]])
            S = multi_dot([H, self.Pbar, H.T]) + self.R
            K = multi_dot([self.Pbar, H.T, inv(S)])
            zdiff = self.z[0] - zhat
            self.xbar += K@(zdiff)
            self.Pbar = (np.eye(3) - K @ H) @ self.Pbar

            # pzt *= det(2*np.pi*S)**(-0.5) * np.exp(-0.5 * multi_dot([zdiff.T, inv(S), zdiff]))

        self.xhat = np.copy(self.xbar)
        self.P = np.copy(self.Pbar)
