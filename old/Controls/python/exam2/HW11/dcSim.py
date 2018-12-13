import sys
sys.path.append('..')  # add parent directory
import numpy as np
import matplotlib.pyplot as plt
import dcParam as P
from dcDynamics import dcDynamics
from dcController import dcController
from signalGenerator import signalGenerator
from plotData import plotData
import seaborn as sns
sns.set_style("white")

# instantiate dc, controller, and reference classes
dc = dcDynamics()
ctrl = dcController()
angle = 20.0*np.pi/180.0
reference = signalGenerator(amplitude=angle, frequency=1, y_offset=0)

# instantiate the simulation plots and animation
dataPlot = plotData()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input = reference.square(t)
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, dc.outputs())  # Calculate the control value
        dc.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    dataPlot.updatePlots(t, ref_input, dc.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
