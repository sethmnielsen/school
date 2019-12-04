import numpy as np
import hw8.params as pm
from utils import wrap

class MDP():
    def __init__(self):
        self.map = pm.rew_map
        self.policy = np.full(pm.rew_map.shape, np.nan)
        self.rew_map = pm.rew_map
        self.value_map = np.copy(self.rew_map)

        self.pf = pm.p_forw
        self.pr = pm.p_right
        self.pl = pm.p_left
        self.iter = 0


        
    def calcValues1(self):
        diff = 1e6
        epsilon = 300
        V_n1 = np.zeros(4)
        V_n2 = np.zeros(4)
        while diff > epsilon:
            temp_diff = []
            for i in range(1, pm.rows-1):
                for j in range(1, pm.cols-1):
                   if self.rew_map[i,j] == pm.r_else:
                        V_n1[0] = self.pf * self.value_map[i+1, j  ]
                        V_n1[1] = self.pr * self.value_map[i  , j+1]
                        V_n1[2] = self.pl * self.value_map[i  , j-1]
                        V_n1[3] = self.rew_map[i,j]
                        V_north  = np.sum(V_n1)

                        V_n2[0] = self.pf * (pm.walls[i+1, j  ] + pm.obs[i+1, j  ] + pm.goal[i+1, j] + self.map[i+1, j])
                        V_n2[1] = self.pr * (pm.walls[i  , j+1] + pm.obs[i  , j+1] + pm.goal[i, j+1] + self.map[i, j+1])
                        V_n2[2] = self.pl * (pm.walls[i  , j-1] + pm.obs[i  , j-1] + pm.goal[i, j-1] + self.map[i, j-1])
                        V_n2[3] = self.rew_map[i,j]
                        V_north2 = np.sum(V_n2)

                        V_south = (self.pf * (pm.walls[i-1, j  ] + pm.obs[i-1, j  ] + pm.goal[i-1, j] + self.map[i-1, j]) + \
                                   self.pr * (pm.walls[i  , j-1] + pm.obs[i  , j-1] + pm.goal[i, j-1] + self.map[i, j-1]) + \
                                   self.pl * (pm.walls[i  , j+1] + pm.obs[i  , j+1] + pm.goal[i, j+1] + self.map[i, j+1])) + self.rew_map[i,j]

                        V_east  = (self.pf * (pm.walls[i  , j+1] + pm.obs[i  , j+1] + pm.goal[i, j+1] + self.map[i, j+1]) + \
                                   self.pr * (pm.walls[i+1, j  ] + pm.obs[i+1, j  ] + pm.goal[i+1, j] + self.map[i+1, j]) + \
                                   self.pl * (pm.walls[i-1, j  ] + pm.obs[i-1, j  ] + pm.goal[i-1, j] + self.map[i-1, j])) + self.rew_map[i,j]

                        V_west  = (self.pf * (pm.walls[i  , j-1] + pm.obs[i  , j-1] + pm.goal[i, j-1] + self.map[i, j-1]) + \
                                   self.pr * (pm.walls[i-1, j  ] + pm.obs[i-1, j  ] + pm.goal[i-1, j] + self.map[i-1, j]) + \
                                   self.pl * (pm.walls[i+1, j  ] + pm.obs[i+1, j  ] + pm.goal[i+1, j] + self.map[i+1, j])) + self.rew_map[i,j]
                        V = [V_north, V_south, V_east, V_west]
                        max = np.max(V)
                        argmax = np.argmax(V)
                        self.policy[i, j] = argmax
                        temp_diff.append(np.abs(self.map[i,j] - max * self.gamma))
                        self.map[i,j] = max * self.gamma
            diff = np.sum(temp_diff)
            self.iter += 1


    def calcValues2(self):
        inds = np.nonzero(self.map)

        diff = 1e6
        epsilon = 1
        idx_r0 = 1
        idx_r = pm.rows - 1
        idx_c0 = 1
        idx_c = pm.cols - 1

        while diff > epsilon:
            #Value for the traveling north reward policy. Need to add the cost of being in that state
            V_north = self.pf * self.map[idx_r0+1:idx_r+1, idx_c0:idx_c] + \
                      self.pr * self.map[idx_r0:idx_r, idx_c0+1:idx_c+1] + \
                      self.pl * self.map[idx_r0:idx_r, idx_c0-1:idx_c-1] 
            #Value for going south
            V_south = self.pf * self.map[idx_r0-1:idx_r-1, idx_c0:idx_c] + self.pr * self.map[idx_r0:idx_r, idx_c0+1:idx_c+1] + self.pl * self.map[idx_r0:idx_r, idx_c0-1:idx_c-1] 
            #Value for going East
            V_east = self.pf * self.map[idx_r0:idx_r, idx_c0+1:idx_c+1] + self.pr * self.map[idx_r0-1:idx_r-1, idx_c0:idx_c] + self.pl * self.map[idx_r0+1:idx_r+1, idx_c0:idx_c]
            #Value for Going West
            V_west = self.pf * self.map[idx_r0:idx_r, idx_c0-1:idx_c-1] + self.pr * self.map[idx_r0-1:idx_r-1, idx_c0:idx_c] + self.pl * self.map[idx_r0+1:idx_r+1, idx_c0:idx_c]

            V = np.stack((V_north, V_south, V_east, V_west), axis=2)
            self.policy = np.argmax(V,axis=2) #use for updating the policy
            max = np.max(V, axis=2) #use for updating map
            debug = 1
            diff = np.sum(max - self.map[idx_r0:idx_r, idx_c0:idx_c])
            self.map[idx_r0:idx_r, idx_c0:idx_c] = max

            #reset obstacles
            idx_walls = np.argwhere(not pm.walls == 0)
            self.map[idx_walls[0,:], idx_walls[1,:]] = -100
            idx_obs = np.argwhere(not pm.obs == 0)
            self.map[idx_obs[0,:], idx_obs[1,:]] = -5000
            idx_goal = np.argwhere(not pm.goal == 0)
            self.map[idx_goal[0,:], idx_goal[1,:]] = np.sign(pm.goal[idx_goal[0,:], idx_goal[1,:]]) * 1e6