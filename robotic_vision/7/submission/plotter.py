#!/usr/bin/env python3
from task1_py import Task1
from task3_py import Task3
import numpy as numpy
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
from IPython.core.debugger import Pdb

DISPLAY = False

def run_task3():
    t3 = Task3()

    z_vec = np.array([])
    z_vec = t3.run(DISPLAY)
    
    skip_frames = 6
    z_vec = z_vec[skip_frames:]
    
    t_fin = z_vec[-2:]

    inds = np.arange(skip_frames+2, z_vec.size+skip_frames+2)
    inds_fin = inds[-2:]

    # Best linear fit
    w_vec = np.ones_like(z_vec)
    w_vec[-5:] = np.ones(5) * 10
    W = np.diag(w_vec)
    A = np.vstack((inds, np.ones_like(inds))).T
    x = np.linalg.pinv(A) @ z_vec
    xw = np.linalg.pinv(W@A) @ W @ z_vec
    
    b = np.arange(skip_frames, 60)
    B = np.vstack((b, np.ones_like(b))).T
    y = B @ x
    yw = B @ xw

    C = np.vstack((inds_fin, np.ones_like(inds_fin))).T
    x2 = np.linalg.pinv(C) @ t_fin
    
    d = np.arange(inds[-2], 30)
    D = np.vstack((d, np.ones_like(d))).T
    y2 = D @ x2

    print('Task3 estimate: ', -xw[1]/xw[0])

    plt.figure(3)
    plt.scatter(inds, z_vec, color='r')
    plt.plot(b, y, label='least squares fit')
    # plt.plot(d, y2, label='last 2 pts')
    # plt.plot(b, yw, label='LS weighted (last 5 pts)')
    plt.legend(loc='upper right')
    plt.xlabel('Frame Number')
    plt.ylabel('Distance to Impact (mm)')
    plt.ylim(bottom=0)
    plt.show()
    

def run_task2():
    t2 = Task1()
    dist = 15.25

    t_vec = np.array([])
    t_vec = t2.run(DISPLAY)
    
    skip_frames = 6
    t_vec = t_vec[skip_frames:]
    
    t_dist = t_vec * dist
    t_fin = t_dist[-2:]

    inds = np.arange(skip_frames+2, t_dist.size+skip_frames+2)
    inds_fin = inds[-2:]

    # Best linear fit
    w_vec = np.ones_like(t_dist)
    w_vec[-5:] = np.ones(5) * 10
    W = np.diag(w_vec)
    A = np.vstack((inds, np.ones_like(inds))).T
    x = np.linalg.pinv(A) @ t_dist
    xw = np.linalg.pinv(W@A) @ W @ t_dist
    
    b = np.arange(skip_frames, 30)
    B = np.vstack((b, np.ones_like(b))).T
    y = B @ x
    yw = B @ xw

    C = np.vstack((inds_fin, np.ones_like(inds_fin))).T
    x2 = np.linalg.pinv(C) @ t_fin
    
    d = np.arange(inds[-2], 30)
    D = np.vstack((d, np.ones_like(d))).T
    y2 = D @ x2

    print('Task2 estimate: ', -xw[1]/xw[0])

    plt.figure(2)
    plt.scatter(inds, t_dist, color='r')
    plt.plot(b, y, label='least squares fit')
    plt.plot(d, y2, label='last 2 pts')
    plt.plot(b, yw, label='LS weighted (last 5 pts)')
    plt.legend(loc='upper right')
    plt.xlabel('Frame Number')
    plt.ylabel('Distance to Impact (mm)')
    plt.ylim(bottom=0)
    # plt.show()


def run_task1(): 
    t1 = Task1()
    t_vec = np.array([])
    t_vec = t1.run(DISPLAY) 
    
    skip_frames = 6
    t_vec = t_vec[skip_frames:]
    t_fin = t_vec[-2:]

    inds = np.arange(skip_frames+2, t_vec.size+skip_frames+2)
    inds_fin = inds[-2:]

    # Best linear fit
    w_vec = np.ones_like(t_vec)
    w_vec[-5:] = np.ones(5) * 10
    W = np.diag(w_vec)
    A = np.vstack((inds, np.ones_like(inds))).T
    x = np.linalg.pinv(A) @ t_vec
    xw = np.linalg.pinv(W@A) @ W @ t_vec
    
    b = np.arange(skip_frames, 30)
    B = np.vstack((b, np.ones_like(b))).T
    y = B @ x
    yw = B @ xw

    C = np.vstack((inds_fin, np.ones_like(inds_fin))).T
    x2 = np.linalg.pinv(C) @ t_fin
    
    d = np.arange(inds[-2], 30)
    D = np.vstack((d, np.ones_like(d))).T
    y2 = D @ x2

    print('Task1 estimate: ', -xw[1]/xw[0])

    plt.figure(1)
    plt.scatter(inds, t_vec, color='r')
    plt.plot(b, y, label='least squares fit')
    plt.plot(d, y2, label='last 2 pts')
    plt.plot(b, yw, label='LS weighted (last 5 pts)')
    plt.legend(loc='upper right')
    plt.xlabel('Frame Number')
    plt.ylabel('Frames to Impact')
    plt.ylim(bottom=0)
    # plt.show()

if __name__ == '__main__':
    
    run_task1()
    run_task2()
    run_task3()