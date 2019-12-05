import numpy as np
import hw8.params as pm
from utils import wrap

class MDP():
    def __init__(self):
        self.map = np.zeros_like(pm.rew_map)
        self.policy = np.full(pm.rew_map.shape, np.nan)
        self.rew_map = pm.rew_map
        self.value_map = np.zeros_like(self.rew_map)
        # self.value_map += pm.goal

        self.pf = pm.p_forw
        self.pr = pm.p_right
        self.pl = pm.p_left
        self.iter = 0

    def post_map_setup(self):
        self.map[pm.walls<0] = pm.r_walls
        self.map[pm.goal>0] = pm.r_goal 
        self.map[pm.obs<0] = pm.r_obs
        self.map = self.map.T 
        self.policy = self.policy.T
        # self.map = np.flip(self.map.T, axis=1)
        # self.policy = np.flip(self.policy.T, axis=1)

        
    def calcValues1(self):
        diff = 1e6
        epsilon = 300
        V_n = np.zeros(4)
        V_s = np.zeros(4)
        V_e = np.zeros(4)
        V_w = np.zeros(4)
        while diff > epsilon:
            temp_diff = []
            for i in range(1, pm.rows-1):
                for j in range(1, pm.cols-1):
                   if self.rew_map[i,j] == pm.r_else:
                        V_n[0] = self.pf * (self.rew_map[i+1, j  ] + self.value_map[i+1, j  ])
                        V_n[1] = self.pr * (self.rew_map[i  , j+1] + self.value_map[i  , j+1])
                        V_n[2] = self.pl * (self.rew_map[i  , j-1] + self.value_map[i  , j-1])
                        V_n[3] = self.rew_map[i,j]
                        V_north  = np.sum(V_n)

                        V_s[0] = self.pf * (self.rew_map[i-1, j  ] + self.value_map[i-1, j  ])
                        V_s[1] = self.pr * (self.rew_map[i  , j-1] + self.value_map[i  , j-1])
                        V_s[2] = self.pl * (self.rew_map[i  , j+1] + self.value_map[i  , j+1])
                        V_s[3] = self.rew_map[i,j]
                        V_south  = np.sum(V_s)

                        V_e[0] = self.pf * (self.rew_map[i  , j+1] + self.value_map[i  , j+1])
                        V_e[1] = self.pr * (self.rew_map[i+1, j  ] + self.value_map[i+1, j  ])
                        V_e[2] = self.pl * (self.rew_map[i-1, j  ] + self.value_map[i-1, j  ])
                        V_e[3] = self.rew_map[i,j]
                        V_east  = np.sum(V_e)

                        V_w[0] = self.pf * (self.rew_map[i  , j-1] + self.value_map[i  , j-1])
                        V_w[1] = self.pr * (self.rew_map[i-1, j  ] + self.value_map[i-1, j  ])
                        V_w[2] = self.pl * (self.rew_map[i+1, j  ] + self.value_map[i+1, j  ])
                        V_w[3] = self.rew_map[i,j]
                        V_west  = np.sum(V_w)

                        V = [V_north, V_south, V_east, V_west]
                        vmax = np.max(V)
                        argmax = np.argmax(V)
                        self.policy[i, j] = argmax
                        temp_diff.append(np.abs(self.value_map[i,j] - vmax * pm.gamma))
                        self.value_map[i,j] = pm.gamma*vmax
            diff = np.sum(temp_diff)
            self.iter += 1
            print(f'diff: {diff}, iter: {self.iter}')


    def calcValues2(self):
        inds = np.nonzero(self.map)

        diff = 1e6
        epsilon = 1
        idx_r0 = 1
        idx_r = pm.rows - 1
        idx_c0 = 1
        idx_c = pm.cols - 1

        while diff > epsilon:
            V_north = self.pf * self.value_map[2:pm.rows, 1:pm.cols-1] + \
                      self.pr * self.value_map[1:pm.rows, 1:pm.cols-1] + \
                      self.pl * self.value_map[1:pm.rows, 1:pm.cols-1] 

            #Value for the traveling north reward policy. 
            V_north = self.pf * self.map[idx_r0+1:idx_r+1, idx_c0  :idx_c  ] + \
                      self.pr * self.map[idx_r0  :idx_r  , idx_c0+1:idx_c+1] + \
                      self.pl * self.map[idx_r0  :idx_r  , idx_c0-1:idx_c-1] 
                      
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