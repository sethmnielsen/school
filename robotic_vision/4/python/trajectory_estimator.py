#!/usr/bin/env python3
from estimate_trajectory_interface import TrajectoryEstimator
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

if __name__ == '__main__':
    trj = TrajectoryEstimator()
    DISPLAY = False
    trj.init(DISPLAY)
    
    pts = np.zeros((100,3));
    for i in range(100):
        pts[i] = trj.run(i)
    
    x = pts[:,0][32:63]
    y = pts[:,1][32:63]
    z = pts[:,2][32:63]

    A = np.array([x, y]).T
    s = np.linalg.inv(A.T @ A) @ A.T @ z
    print('s:', s)

    ### Plotting
    PLOT = True
    if PLOT:
        # fig = plt.figure(dpi=150)
        fig1 = plt.figure()
        # plt.scatter(x, y, label='x and y')
        plt.plot(x, z, label='x and z')
        plt.legend(loc='upper right')
        plt.xlabel('x')
        plt.ylabel('z')

        fig2 = plt.figure()
        plt.plot(y, z, label='y and z')
        plt.legend(loc='upper right')
        plt.xlabel('y')
        plt.ylabel('z')
        plt.show()