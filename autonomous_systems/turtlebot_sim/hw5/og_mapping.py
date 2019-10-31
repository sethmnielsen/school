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

class OGMapping():
    def __init__(self, X, z, thk):
        # self.gridmap = np.zeros((3,100,100))
        # self.gridmap[0] = self.gridmap[0] + np.arange(0.5,100,1.0)
        # self.gridmap[1] = self.gridmap[0].T
        n = pm.n
        self.gridmap = np.zeros((n,n))
        self.inds = np.indices(((n,n)))

        self.d = np.zeros((n,n))
        self.psi = np.zeros((n,n))
        self.inds = np.indices((n,n))

        self.X = X
        self.z_r = z[0]
        self.z_phi = z[0]
        self.thk = thk
    
    def update_map(self, Xt, z_rt, z_phit):
        pos = Xt[:2]
        th = Xt[2]
        self.gridmap += self.inverse_range_sensor_model(pos, th, z_rt, z_phit)

    def inverse_range_sensor_model(self, pos, th, z_r, z_phi):
        logodds = np.zeros((pm.n,pm.n))
        dist_x = self.inds[0] - pos[0]
        dist_y = self.inds[1] - pos[1]
        
        self.d = np.sqrt( dist_x**2 + dist_y**2, out=self.d)
        self.psi = np.arctan2( dist_y, dist_x, out=self.psi ) - th
        angle_diffs = np.abs( self.psi[None,:,:] - z_phi[:,None,None] )
        k = np.argmin(angle_diffs, axis=0)
        
        phi_k = z_phi[k]
        r_k = z_r[k]

        mask_dr = self.d > (r_k + pm.alpha/2)
        mask_psiphi = np.abs( self.psi - phi_k ) > pm.beta/2
        mask0 = mask_dr | mask_psiphi

        mask_occ = ~mask0 & ( np.abs( self.d - r_k ) < pm.alpha/2 )
        mask_free = ~mask_occ & ( self.d <= r_k )

        logodds[mask_occ] = pm.l_occ
        logodds[mask_free] = pm.l_free

        return logodds