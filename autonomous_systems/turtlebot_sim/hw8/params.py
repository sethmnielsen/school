import shared
if shared.USE_CUPY:
    import cupy as xp
else:
    import numpy as xp

import numpy as np
import scipy.io as sio
import sys
sys.path.append("..")



r_obs = -5000
r_goal = 1e6
r_walls = -100
r_else = -2

data = sio.loadmat('matlab_data/mdp_map.mat')
rows = data['Mm'].item()
cols = data['Nm'].item()
obs   = np.array(data['obs'])   * r_obs
goal  = np.array(data['goal'])  * r_goal
walls = np.array(data['walls']) * r_walls
rew_map = walls + obs + goal
rew_map[rew_map == 0] = r_else

del data

x0 = 20
y0 = 28 

# x0 = 28 
# y0 = 20 

p_forw = 0.8
p_left = 0.1
p_right = 0.1
gamma = 1.0