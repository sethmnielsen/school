import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import bobParam as P
from bobDynamics import bobDynamics
from bobController import bobController
from signalGenerator import signalGenerator
from bobAnimation import bobAnimation
from plotData import plotData

# instantiate bob, controller, and reference classes
bob = bobDynamics()
ctrl = bobController()
reference = signalGenerator(amplitude=0.125, frequency=0.03, y_offset=0.25)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = bobAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input = reference.square(t)
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, bob.outputs())  # Calculate the control value
        print "F =", u[0]
        bob.propagateDynamics(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawbob(bob.states())
    dataPlot.updatePlots(t, ref_input, bob.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
