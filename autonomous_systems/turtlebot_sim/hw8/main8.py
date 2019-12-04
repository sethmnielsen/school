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
import matplotlib.pyplot as plt


np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=120)

def drawArrows(ax, map, policy):
    arrow_len = 0.55
    x0 = .375
    w = 0.25
    l = 0.15
    for i in range(1, pm.rows-1):
        for j in range(1, pm.cols-1):
            if np.isnan(policy[i,j]):
                continue 
            elif policy[i,j] == 3: # North
                plt.arrow(j, i + x0, 0, -arrow_len, head_width=w, head_length=l)
            elif policy[i,j] == 2: #South
                plt.arrow(j, i - x0, 0, arrow_len, head_width=w, head_length=l)
            elif policy[i,j] == 0: #East
                plt.arrow(j-x0, i, arrow_len, 0, head_width=w, head_length=l)
            else: #West
                plt.arrow(j + x0, i, -arrow_len, 0, head_width=w, head_length=l)
    return ax

def drawPath(ax, y, x, policy):
    pp_x = x 
    pp_y = y 
    p_x = x 
    p_y = y
    while not np.isnan(policy[y,x]):
        if policy[y,x] == 3: #North
            plt.plot([x, x], [y, y-1], 'r')
            pp_y = p_y
            p_y = y
            y -= 1
        elif policy[y,x] == 2: #South
            plt.plot([x, x], [y, y+1], 'r')
            pp_y = p_y
            p_y = y
            y += 1
        elif policy[y,x] == 0: #East
            plt.plot([x, x+1], [y, y], 'r')
            pp_x = p_x
            p_x = x
            x += 1
        else:
            plt.plot([x, x-1], [y, y], 'r')
            pp_x = p_x
            p_x = x
            x -= 1
        if pp_x == x and pp_y == y:
            break
    return ax

if __name__ == "__main__":
    mdp = MDP()

    mdp.calcValues1()
    mdp.post_map_setup()

    plt.figure(1)
    ax = plt.imshow(mdp.map * 255)
    ax = drawArrows(ax, mdp.map, mdp.policy)
    ax = drawPath(ax, pm.x0, pm.y0, mdp.policy)
    plt.colorbar()

    plt.show()