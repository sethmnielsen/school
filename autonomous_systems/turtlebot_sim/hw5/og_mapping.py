'''
For the poses and measurements included in the .mat file below, use the occupancy grid mapping techniques of chapter 9 (table 9.1 and 9.2) to create a map of the environment. You can assume the environment is well represented by a 100 m by 100 m grid where cells are 1 m square.

The state_meas_data.mat file includes three variables:

    - X: state vector holding (x, y, theta) at each time step
    - z: measurement vector holding (range, bearing) for nine laser range finder measurements at each time step. NaN is reported if a "hit" is not detected.
    - thk: vector of nine range finder pointing angles ranging between -pi/2 (-90 deg) and pi/2 (90 deg). Pointing angles are equally spaced at pi/8 rad (22.5 deg) of separation. 
Use the following parameters for your inverse range sensor model: alpha = 1 m, beta = 5 deg, z_max = 150 m.

Use p(m_i)  = occupied be 0.6 to 0.7 if a "hit" is detected and 0.3 to 0.4 for p(m_i) = occupied if a "hit" is not detected for a particular cell.
'''

import numpy as np
import hw5.params as pm
from utils import wrap

class OGMapping():
    def __init__(self, thk):
        n = pm.n
        self.thk = thk
        self.gridmap = np.zeros((n,n))

        self.d = np.zeros((n,n))
        self.psi = np.zeros((n,n))
        self.inds = np.transpose(np.indices((n,n)), (0,2,1))

    def update_map(self, Xt, z_rt, z_phit):
        pos = Xt[:2]
        th = Xt[2]
        self.gridmap += self.inverse_range_sensor_model(pos, th, z_rt, z_phit)
        return 1 - 1/(1 + np.exp(self.gridmap))

    def inverse_range_sensor_model(self, pos, th, z_r, z_phi):
        logodds = np.zeros((pm.n,pm.n))
        dist_x = self.inds[0] - pos[0]
        dist_y = self.inds[1] - pos[1]
        
        self.d = np.sqrt( dist_x**2 + dist_y**2, out=self.d)
        self.psi = np.arctan2( dist_y, dist_x, out=self.psi ) - th
        self.psi = wrap(self.psi)

        angle_diffs = np.abs( self.psi[None,:,:] - self.thk[:,None,None] )
        # angle_diffs = np.abs( self.psi[None,:,:] - z_phi[:,None,None] )
        k = np.argmin(angle_diffs, axis=0)
        
        phi_k = z_phi[k]
        r_k = z_r[k]
        dphi_k = self.psi - phi_k

        # Conditions - create masked arrays
        mask_dist = self.d > (r_k + pm.alpha/2)
        mask_angle = np.abs( dphi_k ) > pm.beta/2
        mask_unknown = mask_dist | mask_angle

        mask_occ = ~mask_unknown & ( np.abs( self.d - r_k ) < pm.alpha/2 )
        mask_free = ~mask_unknown & ~mask_occ & ( self.d <= r_k )

        logodds[mask_occ] = pm.l_occ
        logodds[mask_free] = pm.l_free

        return logodds.T