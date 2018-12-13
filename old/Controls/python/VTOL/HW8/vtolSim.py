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
freq = 0.08
reference_z = signalGenerator(amplitude=1.5, frequency=freq, y_offset=3)
reference_h = signalGenerator(amplitude=0, frequency=freq, y_offset=3)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = vtolAnimation()

t = P.t_start  # time starts at t_start
t2 = P.t_start + (1/freq)/2.0
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input_lon = reference_h.square(t2)[0]
    ref_input_lat = reference_z.square(t)[0]
    ref_input = [ref_input_lon, ref_input_lat]
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        [F, tau] = ctrl.u(ref_input, vtol.outputs())  # Calculate the control value
        fl = (tau + F*P.d)/(2*P.d)
        fr = F - fl
        th = vtol.states()[2]
        u = np.matrix([[-F*np.sin(th)],
             [F*np.cos(th)],
             [tau]])
        t = t + P.Ts  # advance time by Ts
        t2 = t2 + P.Ts  # advance time by Ts
        vtol.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
        t2 = t2 + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawvtol(vtol.states())
    dataPlot.updatePlots(t, ref_input_lat, vtol.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
