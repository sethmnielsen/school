#!/usr/env python3

import sys
sys.path.append('..')
import numpy as np
from scipy.io import loadmat

from plotter import Plotter
from turtlebot import Turtlebot
from utils import wrap
import params as pm

import pyqtgraph as pg
from hw5.turtlebot_item import TurtleBotItem

np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=160)

tbot = Turtlebot()

animate = True

plotter = Plotter(animate)
tbot.build_vel_and_state()

N = tbot.N
for i in range(N):
    state = tbot.states[:,i]

    #  image plot
    img = pg.ImageItem(border='w')
    turtlebot = TurtleBotItem(X[:,idx], 1.5) 
    view.addItem(img)
    view.addItem(turtlebot)

    # update plot animation
    # plotter.update_mcl_plot(state, mcl.xhat, mcl.Chi, mcl.P.diagonal(), i)

    z = tbot.get_measurements(state, particles=False)
    # mcl.update(tbot.vc[i], tbot.omgc[i], z)

plotter.make_plots()