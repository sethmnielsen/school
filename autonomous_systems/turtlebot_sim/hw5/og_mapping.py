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

class OGMapping():
    def __init__(self, X, z, thk):
        # self.gridmap = np.zeros((3,100,100))
        # self.gridmap[0] = self.gridmap[0] + np.arange(0.5,100,1.0)
        # self.gridmap[1] = self.gridmap[0].T
        self.gridmap = np.zeros((100,100))
        self.alpha = 1
        self.beta = 5
        self.z_max = 150

        self.X = X
        self.z_r = z[0]
        self.z_phi = z[0]
        self.thk = thk
    
    def update_map(self, l):
        for m in self.gridmap:
            # if m (cell) is located within field of view:
            l = l + self.inverse_sensor_model()

    def inverse_range_sensor_model(self):
        pass