import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Initialize variables
m = 100
b = 20
dt = 0.05
t_end = 50
x0 = 0  # initial position guess
v0 = 0  # initial velocity guess
N = int(t_end / dt) # number of samples

# Noise 
delta = 0.001 # measurement noise covariance of position
R = 0.001
eps_x = 0.0001 # process noise covariance of position
eps_v = 0.01 # process noise covariance of velocity
Q = np.array([eps_x, eps_v])
P = np.eye(2)

F = np.zeros(N)
F[:100] = 50
F[500:600] = -50
t_arr = np.arange(0, t_end, dt)

# Plotting
v_arr = np.zeros(N)
x_arr = np.zeros(N)

# True states
x = 0
v = 0
x_eps = 0  # noisy x

# Estimated states
xhat = np.array([x, v])

# State space matrices
A = np.array([[0, 1],
              [0, -b/m]])

B = np.array([0, 1/m])

# Simulation loop
for i in range(N-1):
    ### Dynamics
    # noise
    mean = [0,0]
    cov = [[1,0], 
           [0,1]]
    # equations for truth propagation
    vdot = (F[i] - b*v) / m
    v = v + vdot*dt
    xhat_eps = np.sqrt(Q)*np.random.multivariate_normal(mean, cov)
    x = x + v*dt + np.sign(vdot)*0.5*vdot**2

    # Prediction
    # xbar = np.array([x, vdot])
    xhat_dot = A @ xhat + B*F[i]
    P = A @ P @ A.T  +  Q *dt**2
    
    # Correction
    # xhat = xhat + L*(y_t - C*xhat)

    # Add to plots
    x_arr[i] = x_eps 
    v_arr[i] = v_eps

fig, axs = plt.subplots(3, 1, sharex=True)
axs[0].plot(t, F)
axs[0].set_xlim(0, 50)
axs[0].set_ylim(-50, 50)
axs[0].set_xlabel('time (s)')
axs[0].set_ylabel('F (N)')
axs[0].grid(True)

axs[1].plot(t, v_t, 'tab:orange')
axs[1].set_ylabel('v (m/s)')
axs[1].grid(True)

axs[2].plot(t, x_t, 'tab:green')
axs[2].set_ylabel('x (m)')
axs[2].grid(True)

# fig.tight_layout()
plt.show()