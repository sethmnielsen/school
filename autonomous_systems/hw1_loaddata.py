import numpy as np
import scipy.signal as ss
import scipy.io as sio
import matplotlib
import matplotlib.pyplot as plt

data = sio.loadmat('data_hw1.mat')

# Estimated state
xhat = data['mu0'].flatten()
P = data['Sig0'] # error covariance 
# Force and time arrays
F = data['u'].flatten()
t_arr = data['t'].flatten()
x_true = data['xtr'].flatten()
v_true = data['vtr'].flatten()
z = data['z'].flatten()

# Initialize variables
m = 100
b = 20
dt = 0.05
t_end = 50
N = int(t_end / dt)+1 # number of samples
K = np.zeros(2)  # Kalman gains

# Noise 
delta = 0.001 # measurement noise covariance of position
R = delta  # covariance of the observation noise
eps_x = 0.0001 # process noise covariance of position
eps_v = 0.01 # process noise covariance of velocity
Q = np.diag([eps_x, eps_v]) # covariance of the process noise 
Pbar = np.eye(2) # prediction error covariance 

# Predicted state
xbar = np.array([0, 0])

# State space matrices
A = np.array([[0, 1],
              [0, -b/m]])

B = np.array([[0, 1/m]]).T
C = np.array([[1, 0]])
sys = ss.StateSpace(A, B, C, np.array([[0]]))
sysd = ss.cont2discrete((sys._A, sys._B, sys._C, sys._D), dt)
A = sysd[0]
B = sysd[1].flatten()
C = sysd[2].flatten()

# Plotting
x_state_arr = np.zeros((2,N))
xhat_arr = np.zeros((2,N))
estimate_error_arr = np.zeros((2,N))
error_cov_arr = np.zeros((2,N))
K_arr = np.zeros((2,N))


# noise
mean = [0,0]
cov = [[1,0], 
       [0,1]]
# Simulation loop
for i in range(N-1):
    x_state = np.array([x_true[i], v_true[i]])
    
    xbar = A @ xhat + B*F[i]
    Pbar = A @ P @ A.T  +  Q 
    
    # Measurement Correction
    K = Pbar @ C.T * (C @ Pbar @ C.T + R)**(-1)  # Kalman gain
    xhat = xbar + K * (z[i] - C @ xbar)
    P = (np.eye(2) - np.outer(K, C)) @ Pbar

    # Error
    estimate_error = x_state - xhat
    error_cov = P

    ''' Plots (3):
        1) position and vel states/state estimates vs time
        2) estimation error and error covariance vs time
        3) Kalman gains versus time
    '''
    # Plot 1
    x_state_arr[:,i] = x_state
    xhat_arr[:, i] = xhat

    # Plot 2
    estimate_error_arr[:,i] = estimate_error
    error_cov_arr[:,i] = error_cov.diagonal()

    # Plot 3
    K_arr[:,i] = K


fig, axs = plt.subplots(4, 1, sharex=True)
# subplot 1 - pos, vel truth/estimate
ax_pos = axs[0]
ax_vel = ax_pos.twinx()
lns  = ax_pos.plot(t_arr, x_state_arr[0], color='blue', linestyle='solid', label='x true')
lns += ax_pos.plot(t_arr, xhat_arr[0], color='purple', linestyle='dashed', label='x estimate')
ax_pos.set_xlabel('time (s)')
lns += ax_vel.plot(t_arr, x_state_arr[1], color='green', linestyle='solid', label='v true')
lns += ax_vel.plot(t_arr, xhat_arr[1], color='cyan', linestyle='dashed', label='v estimate')
ax_pos.set_ylabel('position (m)')
ax_pos.set_xlim(0, 50)
# ax_pos.set_ylim(-50, 50)
ax_pos.grid()
# velocity
ax_vel.set_ylabel('velocity (m/s)')
# ax_vel.set_ylim(-20, 20)
labels = [l.get_label() for l in lns]
ax_pos.legend(lns, labels)

##### subplot 2
ax_err = axs[1]
lns = ax_err.plot(t_arr, estimate_error_arr[0], color='orange', linestyle='solid', 
            label='x error estimate')
lns += ax_err.plot(t_arr, estimate_error_arr[1], color='yellow', linestyle='solid', 
            label='v error estimate')
ax_err.set_ylabel('error x: (m), v: (m/s))')
labels = [l.get_label() for l in lns]
ax_err.legend(lns, labels)

#### subplot 3
ax_cov = axs[2]
lns = ax_cov.plot(t_arr, error_cov_arr[0], color='red', linestyle='dashed', 
            label='x error cov')
lns += ax_cov.plot(t_arr, error_cov_arr[1], color='black', linestyle='dashed', 
            label='v error cov')
ax_cov.set_ylabel('covariance')
labels = [l.get_label() for l in lns]
ax_cov.legend(lns, labels)

#### subplot 4
axs[3].plot(t_arr, K_arr[0], color='brown', linestyle='solid', label='K_x')
axs[3].plot(t_arr, K_arr[1], color='gray', linestyle='solid', label='K_v')
axs[3].set_ylabel('Kalman gain')
axs[3].legend()

plt.grid(True)
plt.show()