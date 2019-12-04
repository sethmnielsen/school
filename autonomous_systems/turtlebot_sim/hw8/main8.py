#!/usr/env python3

'''
Implement the discrete value iteration algorithm for MDP's outlined in Table 14.1.

Demonstrate your algorithm by finding the optimal path through the map specified by this Matlab script: MDP_hw_map.m 

Use a discount factor of 1 initially. Assign each cell of the map with a nominal cost of -2. Assign goal cells a reward of +100000, obstacles a cost of -5000, and walls a cost of -100.

Assume that control actions result in your robot moving north, east, south, or west, and that your robot moves in the commanded direction with probability 0.8, 90 deg left of the commanded direction with probability 0.1, and 90 deg right of the commanded direction with probability 0.1.

(1) Create a plot of the optimal policy for the specified map. Here's a function to draw arrows if you care to use it:draw_arrow.m  Download 

(2) Create a plot of the value function for specified map and robot characteristics.

(3) With the robot starting in the initial state (28,20), plot the path to the goal region based on the optimal policy.

(4) Exercise your algorithm by changing the map, the initial condition on the robot location, the costs/rewards in the map, the discount factor, and the uncertainty model associated with the robot motion p(xj | u, xi). Does the algorithm give the results you'd expect?
'''

import sys
sys.path.append('..')
import numpy as np

from utils import wrap
import params as pm
from mdp import MDP

np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=120)

if __name__ == "__main__":
    mdp = MDP()

    mdp.calcValues1()
    # mdp.correcStaticCells()

    # plt.figure(1)
    # ax = plt.imshow(mdp.map * 255)
    # ax = drawArrows(ax, mdp.map, mdp.policy)
    # ax = drawPath(ax, params.x0, params.y0, mdp.policy)
    # plt.colorbar()

    # plt.show()