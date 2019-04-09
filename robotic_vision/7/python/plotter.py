#!/usr/bin/env python3
from task1_py import Task1
import numpy as numpy
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
from IPython.core.debugger import Pdb

if __name__ == '__main__':
    t1 = Task1();
    DISPLAY = False
    
    t_vec = np.array([])
    t_vec = t1.run(DISPLAY)
    
    skip_frames = 6
    t_vec = t_vec[skip_frames:]
    t_fin = t_vec[-2:]

    inds = np.arange(skip_frames+2, t_vec.size+skip_frames+2)
    inds_fin = inds[-2:]

    # Best linear fit
    w_vec = np.ones_like(t_vec)
    w_vec[-4:] = [5,5,5,5]
    W = np.diag(w_vec)
    A = np.vstack((inds, np.ones_like(inds))).T
    x = np.linalg.pinv(A) @ t_vec
    
    b = np.arange(skip_frames, 30)
    B = np.vstack((b, np.ones_like(b))).T
    y = B @ x

    C = np.vstack((inds_fin, np.ones_like(inds_fin))).T
    x2 = np.linalg.pinv(C) @ t_fin
    
    d = np.arange(inds[-2], 30)
    D = np.vstack((d, np.ones_like(d))).T
    y2 = D @ x2


    plt.figure(1)
    plt.scatter(inds, t_vec, color='r')
    plt.plot(b, y)
    plt.plot(d, y2)
    plt.xlabel('Frame Number')
    plt.ylabel('Frames to Impact')
    plt.ylim(bottom=0)
    plt.show()