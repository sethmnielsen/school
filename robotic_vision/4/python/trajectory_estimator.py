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
    PLOT = False
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

    # A = np.array([x, y]).T
    A = np.array([z[:-1], z[1:]]).T
    A_ac = np.vstack([[z[0], 0], A, [0, z[-1]]])

    xd = np.hstack([ x[1:], [0,0] ])
    yd = np.hstack([ y[1:], [0,0] ])
    hx = np.linalg.inv(A_ac.T @ A_ac) @ A_ac.T @ xd
    hy = np.linalg.inv(A_ac.T @ A_ac) @ A_ac.T @ yd

    print('A:\n', A_ac)
    print('hx:\n', hx)
    print('hy:\n', hy)
    
    Pdb().set_trace()

    #### Problem 12 part a ####

    # d = np.array([1, 1, 2, 3, 5, 8, 13])

    # A = np.array([[1, 1],
    #               [2, 1],
    #               [3, 2],
    #               [5, 3],
    #               [8, 5],
    #               [13, 8]])

    # A_ac = np.vstack([[1, 0], A, [0, 13]])
    # R_ac = A_ac.T @ A_ac

    # #### Part b ####
    # ## i
    # A_ = A[:-1]
    # a = np.linalg.inv(A_.T @ A_) @ A_.T @ d[2:]

    # ## ii
    # d_ac = np.hstack([ d[1:], [0,0] ])
    # a_ac = np.linalg.inv(A_ac.T @ A_ac) @ A_ac.T @ d_ac

    ### Plotting
    if PLOT:
        fig1 = plt.figure()
        plt.plot(z[1:], xd, label='x and z')
        plt.plot(z, A_ac @ hx)
        plt.legend(loc='upper right')
        plt.xlabel('x')
        plt.ylabel('z')

        fig2 = plt.figure()
        plt.plot(y, z, label='y and z')
        plt.legend(loc='upper right')
        plt.xlabel('y')
        plt.ylabel('z')
        plt.show()