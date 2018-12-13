import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import vtolParam as P
from vtolDynamics import vtolDynamics
from vtolController import vtolController
from signalGenerator import signalGenerator
from vtolAnimation import vtolAnimation
from plotData import plotData
import seaborn as sns
sns.set_style("white")

# instantiate vtol, controller, and reference classes
vtol = vtolDynamics()
ctrl = vtolController()
freq = 0.01
reference_z = signalGenerator(amplitude=2.5, frequency=freq, y_offset=3)
reference_h = signalGenerator(amplitude=1, frequency=0.02, y_offset=3.01)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = vtolAnimation()

t = P.t_start  # time starts at t_start
t2 = P.t_start + (1/freq)/2.0
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input_lon = reference_h.square(t2)[0]
    ref_input_lat = reference_z.square(t)[0]
    ref_input = [ref_input_lat, ref_input_lon]
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        [fl, fr] = ctrl.u(ref_input, vtol.states())  # Calculate the control value
        u = [fl, fr]
        vtol.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
        t2 = t2 + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawvtol(vtol.states())
    dataPlot.updatePlots(t, ref_input, vtol.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
