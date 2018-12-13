import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import msd2Param as P
from msd2Dynamics import msd2Dynamics
from msd2Controller import msd2Controller
from signalGenerator import signalGenerator
from plotData import plotData
from plotObserverData import plotObserverData
import seaborn as sns
sns.set_style("white")

# instantiate msd2, controller, and reference classes
msd2 = msd2Dynamics()
ctrl = msd2Controller()
reference = signalGenerator(amplitude=2.5, frequency=0.05, y_offset=0)

# instantiate the simulation plots and animation
dataPlot = plotData()
observerPlot = plotObserverData()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input = reference.square(t)
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, msd2.states())  # Calculate the control value
        sys_input = [u[0]]  # input to plant is control input + disturbance (formatted as a list)
        msd2.propagateDynamics(sys_input)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    dataPlot.updatePlots(t, ref_input, msd2.states(), u)
    observerPlot.updatePlots(t, msd2.states(), ctrl.x_hat)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
