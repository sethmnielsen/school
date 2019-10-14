from IPython.core.debugger import set_trace
# import importlib as imp
from importlib import reload

import numpy as np
import scipy as sp
import scipy.io as sio

blah = sio.loadmat('hw1_soln_data.mat')
x_mcl = np.vstack(([blah['xtr'],blah['vtr']]))
z_mcl = blah['z'][0]

import matplotlib.pyplot as plt

mod_switch = 0

if mod_switch == 0:
    import hw1_auv
    reload(hw1_auv)
    from hw1_auv import UUV
elif mod_switch == 1:
    import hw1_auv_linear # as auv
    reload(hw1_auv_linear)
    from hw1_auv_linear import UUV
#

# vv = imp.import_module(my_mod)
# reload(vv)
# from vv import UUV

uuv = UUV(x_mcl, z_mcl)

uuv.kf_run()

#
f1 = plt.figure(1)
f1.clf()
ax1 = plt.axes()

pt1_1 = plt.plot(uuv.tt_hist, uuv.pos_tru, label='True: pos')
pt1_2 = plt.plot(uuv.tt_hist, uuv.vel_tru, label='True: vel')
pt1_3 = plt.plot(uuv.tt_hist, uuv.pos_est, label='Est: pos')
pt1_4 = plt.plot(uuv.tt_hist, uuv.vel_est, label='Est: vel')

ax1.legend()
f1.show()

# ==================

f2 = plt.figure(2)
f2.clf()
ax2 = plt.axes()

pt2_1 = plt.plot(uuv.tt_hist, uuv.err_est_pos, label='Error: pos')
pt2_2 = plt.plot(uuv.tt_hist, uuv.err_cov_pos, label='Error Cov.: pos')
pt2_3 = plt.plot(uuv.tt_hist, uuv.err_cov_npos, label='-Error Cov.: pos')

ax2.legend()
f2.show()

# ==================

f3 = plt.figure(3)
f3.clf()
ax3 = plt.axes()

pt3_1 = plt.plot(uuv.tt_hist, uuv.err_est_vel, label='Error: vel')
pt3_2 = plt.plot(uuv.tt_hist, uuv.err_cov_vel, label='Error Cov.: vel')
pt3_2 = plt.plot(uuv.tt_hist, uuv.err_cov_nvel, label='-Error Cov.: vel')

ax3.legend()
f3.show()

# ==================

f4 = plt.figure(4)
f4.clf()
ax4 = plt.axes()

pt4_1 = plt.plot(uuv.tt_hist, uuv.K_gain_pos, label='K gain: pos')
pt4_1 = plt.plot(uuv.tt_hist, uuv.K_gain_vel, label='K gain: vel')

ax4.legend()
f4.show()

#

# lowered force, and everything acted normally

# when I lower the model uncertainty for velocity, the *true* state behaves
# much closer to what would really happen, due to the much smaller noisy_state
# propagation

# When I raise my position uncertainty, everything is much more jagged, but
# the system stays in the covariance bounds

# When I raise the initial velocity to 10, the filter still catches up very
# quickly to the correct estimate.

# when I raise the initial position, because the dynamics are perfect, there is
# no error off the bat

# increasing my measurement noise made the initial spike in Kalman gain be a
# a little lower, and the overall settled gain be *much* lower, compared to
# lowering the measurement noise

#
