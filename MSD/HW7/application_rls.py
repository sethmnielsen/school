import numpy as np
np.set_printoptions(precision=3)

m = 3     # number of parameters (k, b, m)
n = 1000  # iterations

h = np.array([1,2,3,4,5])  # impulse response
hhat = np.zeros(m)         # initial estimated parameters
f = np.random.randn(n)     # normally-distributed random input
fn = np.hstack(([0,0,0,0],f))  # convenience array used to shift through input (f)
q = np.zeros(m)  # input data for one time step
delta = .0001
P = 1/delta * np.eye(m)  # initial P

for i in range(n):
    d = fn[i:i+5] @ h  # true output
    q = fn[i:i+m]      # q update

    k = P @ q / (1 + q.T @ P @ q)  # kalman gain vector
    y = q @ hhat  # filter output
    e = d - y     # error

    hhat = hhat + k * e  # update of estimated parameters
    P = P - k * q @ P    # P update1

print('hhat:',hhat)


########################################################################################

import sys
sys.path.append('..')  # add parent directory
import numpy as np
import msdParam as P
from msdDynamics import msdDynamics
from msdController import msdController
from signalGenerator import signalGenerator


# instantiate msd, controller, and reference classes
msd = msdDynamics()
ctrl = msdController()
reference = signalGenerator(amplitude=30*np.pi/180.0, frequency=0.05)

# u - input
# msd.states() - true output

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input = reference.sin(t)
    # ref_input = [1]
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, msd.outputs())  # Calculate the control value
        msd.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts





###########################################################################################

# import matplotlib.pyplot as plt
# from msdAnimation import msdAnimation
# from plotData import plotData
# import seaborn as sns
# sns.set_style("white")
#
# # instantiate the simulation plots and animation
# dataPlot = plotData()
# animation = msdAnimation()
#
#
#     # update animation and data plots
#     # animation.drawmsd(msd.states())
#     # dataPlot.updatePlots(t, ref_input, msd.states(), u)
#     # plt.pause(0.000001)  # the pause causes the figure to be displayed during the sim
#
# # Keeps the program from closing until the user presses a button.
# # print('Press key to close')
# # plt.waitforbuttonpress()
# # plt.close()
