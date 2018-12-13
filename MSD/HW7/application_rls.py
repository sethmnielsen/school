import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import numpy as np
import msdParam as param
from msdDynamics import msdDynamics
from msdController import msdController
from signalGenerator import signalGenerator
from msdAnimation import msdAnimation
from plotData import plotData
import seaborn as sns
sns.set_style("white")
np.set_printoptions(precision=3)

msd = msdDynamics()
ctrl = msdController()

# dataPlot = plotData()
# animation = msdAnimation()
reference = signalGenerator(amplitude=10, frequency=0.1)

# u - input (f)
# msd.outputs()[0]: z - true output (d)

m = 3     # number of parameters (k, b, m)
n = 100  # iterations

hhat = np.zeros(m)         # initial estimated parameters

h = np.array([param.b/param.m, param.k/param.m, 1/param.m])
f = np.random.randn(n)*5 + 2.5     # normally-distributed random input
fn = np.hstack(([0,0],f))  # convenience array used to shift through input (f)
q = np.zeros(m)  # input data for one time step
delta = .00001
P = 1/delta * np.eye(m)  # initial P

d_arr = np.zeros(n)
y_arr = np.zeros(n)
t_arr = np.zeros(n)

t = param.t_start  # time starts at t_start
for i in range(n):
    # x = msd.states()
    ref_input = reference.sin(t)
    msd.propagateDynamics(ref_input)  # Propagate the dynamics
    # msd.propagateDynamics([f[i]])  # Propagate the dynamics
    d = msd.outputs()[0]
    # d = msd.states()
    # d = fn[i:i+3] @ h
    # q = fn[i:i+3]
    # q = np.hstack((ref_input[0],q[:-1]))  # q update
    q = np.hstack((ref_input[0],q[:-1]))  # q update

    k = P @ q / (1 + q.T @ P @ q)  # kalman gain vector
    y = q @ hhat  # filter output
    e = d - y     # error

    hhat = hhat + k * e  # update of estimated parameters
    P = P - k * q @ P    # P update

    t_arr[i] = t
    d_arr[i] = d
    y_arr[i] = y

    t = t + param.Ts  # advance time by Ts

    # d = fn[i:i+3] @ h  # true output
    # q = fn[i:i+m]      # q update
    #
    # k = P @ q / (1 + q.T @ P @ q)  # kalman gain vector
    # y = q @ hhat  # filter output
    # e = d - y     # error
    #
    # hhat = hhat + k * e  # update of estimated parameters
    # P = P - k * q @ P    # P update

    # t = t + param.Ts  # advance time by Ts


    # ref_input = reference.random(t)
    # u = [np.random.rand()*3]



    # Propagate dynamics in between plot samples
    # t_next_plot = t + param.t_plot
    # while t < t_next_plot: # updates control and dynamics at faster simulation rate
        # u = ctrl.u(ref_input, msd.outputs())  # Calculate the control value
        # msd.propagateDynamics(u)  # Propagate the dynamics
        # t = t + param.Ts  # advance time by Ts



    # update animation and data plots
    # animation.drawmsd(msd.states())
    # dataPlot.updatePlots(t, ref_input, msd.states(), u)
    # plt.pause(0.000001)  # the pause causes the figure to be displayed during the sim

print('hhat:',hhat)
print('h   :',h)
print('d:', d)
print('y:', y)
print('states:', msd.states())
# Keeps the program from closing until the user presses a button.
# print('Press key to close')

s = 0
fig1 = plt.figure(dpi=150)
plt.plot(t_arr[s:], d_arr[s:], label='d')
plt.xlabel('t')
plt.ylabel('d')

# fig2 = plt.figure(dpi=150)
# plt.plot(t_arr[s:], y_arr[s:], label='y')
# plt.xlabel('t')
# plt.ylabel('y')

# fig3 = plt.figure(dpi=150)
# plt.plot(t_arr[-s:], e_arr[-s:], label='e')
# plt.xlabel('t')
# plt.ylabel('e')

plt.show()
plt.waitforbuttonpress()
plt.close()
