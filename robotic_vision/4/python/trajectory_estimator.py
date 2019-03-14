#!/usr/bin/env python3
from estimate_trajectory_interface import TrajectoryEstimator
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
from IPython.core.debugger import Pdb

if __name__ == '__main__':
    trj = TrajectoryEstimator()
    DISPLAY = False
    PLOT = True
    trj.init(DISPLAY)
    
    pts = np.zeros((100,3));
    for i in range(100):
        pts[i] = trj.run(i)
        if pts[i,0] != 0:
            print(i, ':', pts[i])
    
    begin = 32
    end = 63
    x = pts[:,0][begin:end]
    y = pts[:,1][begin:end]
    z = pts[:,2][begin:end]

    ### Plotting
    if PLOT:
        fig1 = plt.figure()
        # plt.plot(zv[1:], xv, label='xv and zv')
        plt.plot(z, x, label='x and z')
        plt.legend(loc='upper right')
        plt.xlabel('z')
        plt.ylabel('x')

        fig2 = plt.figure()
        plt.plot(z, y, label='y and z')
        plt.legend(loc='upper right')
        plt.xlabel('z')
        plt.ylabel('y')
        plt.show()