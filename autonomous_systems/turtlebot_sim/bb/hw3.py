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
import hw3_ukf
import hw2_anim_plot
reload(lmd)
reload(hw2_tbot)
reload(hw3_ukf)
reload(hw2_anim_plot)
from hw2_tbot import TurtleBot
from hw3_ukf import Ukf
from hw2_anim_plot import TbotPlot

tbot = TurtleBot()

tbot.run_dynamics_sim()

tbot.check_zz()

est = Ukf(tbot)

est.ukf_localize()

est_err, sqrt_cov = lmd.calc_est_error(tbot,est)

# set_trace()


# ======================================
# ======================================

tbplot = TbotPlot(tbot, est, est_err, sqrt_cov)



# ======================================
# ======================================
# ======================================
