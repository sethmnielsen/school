#!/usr/bin/python3

import math
import numpy as np
import random
import time
import warnings

np.seterr(all='ignore')

class StateNode:
    def __init__(self, params=None, root=False, cities=None):
        if root:
            self.city = cities[0]
            self.path = np.array([self.city])
            self.cities_left = np.array(cities[1:])
            self.lb = 0
            self.costmat = self.create_costmat(cities)
            self.keyvalue = 0
        else:
            self.keyvalue = 0
            self.city = params[0]
            self.path = params[1]
            self.cities_left = params[2]
            self.lb = params[3]
            self.costmat = self.reduce_costmat(params[4])

    def create_costmat(self, cities):
        cities = np.array(cities)
        costmat = np.zeros((cities.size,cities.size))
        for i in range(costmat.shape[0]):
            for j in range(costmat.shape[0]):
                costmat[i][j] = cities[i].costTo(cities[j])
        return self.reduce_costmat(costmat, root=True)

    def reduce_costmat(self, costmat, root=False):
        if not root:
            parent_node = self.path[-1]
            parent = parent_node._index
            current = self.city._index
            self.lb += costmat[parent][current]
            costmat[parent] = np.nan  # row = from city
            costmat[:,current] = np.nan    # col = to city
            costmat[current][parent] = np.nan
            self.path = np.append(self.path, self.city)
            city_ind = np.argwhere(self.cities_left==self.city)
            self.cities_left = np.delete(self.cities_left, city_ind)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            row_mins = np.nanmin(costmat, axis=1)
            c = (costmat.T - row_mins).T
            col_mins = np.nanmin(c,axis=0)
            reduced_costmat = c - col_mins

        self.lb += np.nansum((row_mins,col_mins))
        self.keyvalue = self.lb / self.path.size + np.random.random()
        # print("\nReducing costmat for {}-->{}:".format(self.print_path(), self.city._name))
        # print(costmat)
        # print("Costmat reduced:\n",reduced_costmat)
        # print('row_mins:',row_mins)
        # print('col_mins:',col_mins)
        # print('Lower bound:',self.lb)
        # print('keyvalue:',self.keyvalue)
        return reduced_costmat

    def expand(self):
        children = np.array([],dtype=object)
        for i in range(self.cities_left.size):
            next_city = self.cities_left[i]
            if not np.isnan(self.costmat[self.city._index][next_city._index]):
                params = [next_city, np.copy(self.path), np.copy(self.cities_left), self.lb, np.copy(self.costmat)]
                new_node = StateNode(params)
                children = np.append(children, new_node)
        return children

    def print_path(self):
        s = 'A'
        for i in range(1,self.path.size-1):
            s += '-' + self.path[i]._name
        return s

    def print_path_full(self):
        s = 'A'
        for i in range(1,self.path.size):
            s += '-' + self.path[i]._name
        return s
