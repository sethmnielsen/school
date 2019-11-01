import numpy as np

alpha = 1.  # 2 is better?
beta = np.radians(2)   # 5 from specs
n = 102
z_max = 150

l_occ = np.log( 0.65 / (1 - 0.65) )
l_free = np.log( 0.35 / (1 - 0.35) )

# t_arr = np.arange(759)