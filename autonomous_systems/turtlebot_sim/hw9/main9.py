#!/usr/env python3

import sys
sys.path.append('..')
import numpy as np

from utils import wrap
import params as pm
from mdp import MDP
import matplotlib.pyplot as plt


np.set_printoptions(precision=3, suppress=True, sign=' ', linewidth=120)

if __name__ == "__main__":
    mdp = MDP()

    mdp.calcValues1()
    mdp.post_map_setup()

    plt.figure(1)
    ax = plt.imshow(mdp.map * 255)
    plt.colorbar()

    plt.show()