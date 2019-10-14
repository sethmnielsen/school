from IPython.core.debugger import set_trace
# import importlib as imp
from importlib import reload

import numpy as np
import scipy as sp
import scipy.io as sio

import time

# blah = sio.loadmat('hw1_soln_data.mat')
# x_mcl = np.vstack(([blah['xtr'],blah['vtr']]))
# z_mcl = blah['z']

# set_trace()

# import matplotlib.pyplot as plt
# import matplotlib.patches as ptc

# plt.ion()

import lmd
import hw2_tbot
import hw2_ekf
import hw2_anim_plot
reload(lmd)
reload(hw2_tbot)
reload(hw2_ekf)
reload(hw2_anim_plot)
from hw2_tbot import TurtleBot
from hw2_ekf import Ekf
from hw2_anim_plot import TbotPlot

tbot = TurtleBot()

tbot.run_dynamics_sim()

tbot.check_zz()

est = Ekf(tbot)

est.ekf_localize()

est_err, sqrt_cov = lmd.calc_est_error(tbot,est)

# set_trace()


# ======================================
# ======================================

tbplot = TbotPlot(tbot, est, est_err, sqrt_cov)



# ======================================
# ======================================
# ======================================

# The motion model doesn't work in straight line motion because it would
# have a zero in the denominator

# rng and brng measurements are correct!

# When I raise the velocity *5 the error stays quite good. However, when I
# only raise the omega command *5, it turns so fast that the estimates get
# a little worse (by about 25%), and they are much more jagged

# raising the range sigma just makes it take a bit longer to converge
# raising sigma phi didn't change the result too much

# raising alpha *5 made the true state so jagged the filter didn't respond,
# just filtered it mostly smoothly, with similar results for the others


#
