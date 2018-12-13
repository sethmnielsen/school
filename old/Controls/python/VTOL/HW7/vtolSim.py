import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import numpy as np
import vtolParam as P
from vtolDynamics import vtolDynamics
from vtolController import vtolController
from signalGenerator import signalGenerator
from vtolAnimation import vtolAnimation
from plotData import plotData

# instantiate vtol, controller, and reference classes
vtol = vtolDynamics()
ctrl = vtolController()
reference = signalGenerator(amplitude=1, frequency=0.05, y_offset=2)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = vtolAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    # ref_input_lon = reference.square(t)
    ref_input_lon = [3]
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        F = ctrl.u(ref_input_lon, vtol.outputs())  # Calculate the control value
        # tau = ctrl.u(ref_input_lat, vtol.outputs())  # Calculate the control value
        th = vtol.states()[2]
        u = np.matrix([[-F[0]*np.sin(th)],
             [F[0]*np.cos(th)],
             [0]])
        t = t + P.Ts  # advance time by Ts
        vtol.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawvtol(vtol.states())
    dataPlot.updatePlots(t, ref_input_lon, vtol.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
