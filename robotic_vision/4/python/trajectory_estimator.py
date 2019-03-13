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

    #### Problem 12 part a ####

    d = np.array([1, 1, 2, 3, 5, 8, 13])

    A = np.array([[1, 1],
                  [2, 1],
                  [3, 2],
                  [5, 3],
                  [8, 5],
                  [13, 8]])

    R = A.T @ A

    A_ac = np.vstack([[1, 0], A, [0, 13]])
    R_ac = A_ac.T @ A_ac

    #### Part b ####
    ## i
    A_ = A[:-1]
    a = np.linalg.inv(A_.T @ A_) @ A_.T @ d[2:]

    ## ii
    d_ac = np.hstack([ d[1:], [0,0] ])
    a_ac = np.linalg.inv(A_ac.T @ A_ac) @ A_ac.T @ d_ac

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