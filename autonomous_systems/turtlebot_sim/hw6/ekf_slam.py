#! usr/env/python
'''
For this assignment, you are to modify your EKF localization algorithm and simulation to become an EKF SLAM algorithm and simulation.

1) For starters, assume that your sensor is omnidirectional with unlimited range. This means that your sensor can see all landmarks all the time. Show that your EKF SLAM algorithm works by plotting the state estimates (robot pose and landmark locations) against the true states and showing they track/converge. You will likely want to use a few landmarks (<10) to get your algorithm working and debugged. Once it is working, you can increase the number of landmarks. Show that increasing the number of landmarks improves the state estimation accuracy.

2) Plot the final covariance matrix values to illustrate the correlation between landmark states.

3) Narrow the field of view of your sensor to 180 deg, 90 deg, and 45 deg. How does this affect the localization and mapping results? Create an animation of landmark true locations, estimated locations, and estimation covariance (ellipses, 2-sigma) versus time for your simulation.

4) Create a loop-closing scenario with a narrow FOV sensor on your robot. Show how closing the loop (seeing landmarks for second time), results in a drop in landmark location uncertainty for recently viewed landmarks.
'''
import numpy as np
import hw6.params as pm
from utils import wrap

class EKF_SLAM():
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