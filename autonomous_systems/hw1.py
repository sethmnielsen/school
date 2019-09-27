import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt

# Initialize variables
m = 100
b = 20
dt = 0.05
t_end = 50
N = int(t_end / dt) # number of samples
K = np.zeros(2)  # Kalman gains

# Noise 
delta = 0.001 # measurement noise covariance of position
R = delta  # covariance of the observation noise
eps_x = 0.0001 # process noise covariance of position
eps_v = 0.01 # process noise covariance of velocity
Q = np.diag([eps_x, eps_v]) # covariance of the process noise 
P = np.eye(2)  # error covariance (x_state - xhat)
Pbar = np.eye(2) # prediction error covariance (x_state - xbar)

# Force and time arrays
F = np.zeros(N)
F[:100] = 50
F[500:600] = -50
t_arr = np.arange(0, t_end, dt)

# True state
x = 0
v = 0
x_state = np.array([x, v])  # true state, with noise added

# Predicted state
xbar = np.array([0, 0])

# Estimated state
x0 = 0  # initial position guess
v0 = 0  # initial velocity guess
xhat = np.array([x0, v0])

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


# Plot 1
x_state_arr[:,0] = x_state
xhat_arr[:, 0] = xhat

# Plot 2
estimate_error_arr[:,0] = np.copy(xhat)
error_cov_arr[:,0] = P.diagonal()

# Plot 3
K_arr[:,0] = K

# noise
mean = [0,0]
cov = [[1,0], 
       [0,1]]
# Simulation loop
for i in range(1,N-1):
    ### Dynamics

    # truth propagation
    vdot = (F[i] - b*v) / m
    # v = v + vdot*dt
    # eps_x, eps_v = np.sqrt(Q)@np.random.multivariate_normal(mean, cov)
    # x = (x + eps_x) + (v + eps_v)*dt + np.sign(vdot)*0.5*vdot**2
    # x_state = np.array([x, v])
    x_state = A @ x_state + B * F[i] + np.sqrt(Q)@np.random.multivariate_normal(mean, cov)

    # Prediction
    xbar = A @ xhat + B*F[i]
    Pbar = A @ P @ A.T  +  Q 
    
    # Measurement Correction
    K = Pbar @ C.T * (C @ Pbar @ C.T + R)**(-1)  # Kalman gain
    z = x_state[0] + np.sqrt(R) * np.random.randn()
    xhat = xbar + K * (z - C @ xbar)
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
ax_pos = axs[1]
ax_pos.plot(t_arr, estimate_error_arr[0], color='orange', linestyle='solid', 
            label='x error estimate')
ax_pos.plot(t_arr, 2*np.sqrt(error_cov_arr[0]), color='red', linestyle='dashed', 
            label='x error cov')
ax_pos.plot(t_arr, -2*np.sqrt(error_cov_arr[0]), color='red', linestyle='dashed')
ax_pos.set_ylabel('position (m)')
ax_pos.legend()

ax_vel = axs[2]
ax_vel.plot(t_arr, estimate_error_arr[1], color='yellow', linestyle='solid', 
            label='v error estimate')
ax_vel.plot(t_arr, 2*np.sqrt(error_cov_arr[1]), color='black', linestyle='dashed', 
            label='v error cov')
ax_vel.plot(t_arr, -2*np.sqrt(error_cov_arr[1]), color='black', linestyle='dashed')
ax_vel.set_ylabel('velocity (m/s)')
ax_vel.legend()

#### subplot 4
axs[3].plot(t_arr, K_arr[0], color='brown', linestyle='solid', label='K_x')
axs[3].plot(t_arr, K_arr[1], color='gray', linestyle='solid', label='K_v')
axs[3].set_ylabel('Kalman gain')
axs[3].legend()

plt.grid(True)
plt.show()