import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Initialize variables
m = 100
b = 20
Ts = 0.05
t_end = 50
delta = 0.001 # measurement noise covariance of position
eps_x = 0.0001 # process noise covariance of position
eps_v = 0.01 # process noise covariance of velocity
x0 = 0  # initial position guess
v0 = 0  # initial velocity guess
N = int(t_end / Ts) # number of samples
R_0 = np.eye(2)

F = np.zeros(N)
F[:100] = 50
F[500:600] = -50
t = np.arange(0, t_end, Ts)
# True states
v_t = np.zeros(N)
x_t = np.zeros(N)
# Estiamted states
vhat = 0
xhat = 0

# Simulation loop
for i in range(N-1):
    # Dynamics
    vdot = (F[i] - b*v_t[i]) / m
    v_t[i+1] = v_t[i] + vdot*Ts
    x_t[i+1] = x_t[i] + v_t[i]*Ts + np.sign(vdot)*0.5*vdot**2

    # Prediction
    vhat = vhat + vhat* + B*u
    
    # Correction
    xhat = xhat + L*(y_t - C*xhat)

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
