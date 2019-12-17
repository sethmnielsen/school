import numpy as  np

ekf_pos = np.load("results/ekf_position.npz")
ekf_rangebear = np.load("results/ekf_rangebearing.npz")
pf_bear = np.load("results/pf_bearing.npz")
pf_pos = np.load("results/pf_position.npz")

def print_items(data):
    for item in data.items():
        print(item)

def print_values(data):
    for item in data.values():
        print(item)

def print_shapes(data):
    for item in data.values():
        print(item.shape)

def print_keys(data):
    for item in data.keys():
        print(item)