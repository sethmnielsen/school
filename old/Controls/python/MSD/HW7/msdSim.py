import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import numpy as np
import msdParam as P
from msdDynamics import msdDynamics
from msdController import msdController
from signalGenerator import signalGenerator
from msdAnimation import msdAnimation
from plotData import plotData
import seaborn as sns
sns.set_style("white")

# instantiate msd, controller, and reference classes
msd = msdDynamics()
ctrl = msdController()
reference = signalGenerator(amplitude=30*np.pi/180.0, frequency=0.05)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = msdAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    # ref_input = reference.square(t)
    ref_input = [1]
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, msd.outputs())  # Calculate the control value
        msd.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawmsd(msd.states())
    dataPlot.updatePlots(t, ref_input, msd.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
