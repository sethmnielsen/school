#!/usr/bin/env python
import random
import numpy as np
import math
import warnings
from scipy import stats
from .matrix import Matrix
from IPython.core.debugger import Pdb

np.seterr(all='ignore')

class KMeansLearner:
    def __init__(self):
        self.k = 5
        np.random.seed(0)

    def train(self, features):
        self.sse_list = np.zeros(self.k)
        self.cluster_list = np.zeros(self.k)
        self.SSE = 1
        self.random = True

        # Initialize training
        self.n = features.rows
        self.m = features.cols
        self.convert_numpy(features)
        if self.random:
            self.random_init()
        else:
            self.cents = np.copy(self.feats[0:self.k])

        # Begin training loop
        iterations = 0
        save_sse = 0
        while save_sse != self.SSE:
            save_sse = self.SSE
            iterations += 1
            dists = self.calc_dists(self.feats, self.cents)
            cluster_inds = dists.argmin(axis=1)
            self.new_centroids(dists, cluster_inds)  # SSE for current iteration updated here

        sil_score = self.find_silhouette(cluster_inds)

        print('\n##### K-MEANS OUTPUT FOR K = {} #####'.format(self.k))
        print('Number of iterations:', iterations)
        print('Number of clusters:', self.k)
        print('Final cluster centroids:')
        self.print_centroids(features)
        print('For each cluster:')
        self.print_clusters_info()
        print('Total SSE: {:1.3f}'.format(self.SSE))
        print('Total silhouette score: {:1.3f}'.format(sil_score))

    def random_init(self):
        cents_init = np.random.randint(0,self.n,self.k)
        self.cents = np.copy(self.feats[cents_init])

    def convert_numpy(self, features):
        self.feats = np.zeros((features.rows, features.cols))
        for i in range(features.rows):
            self.feats[i] = features.row(i)

        # isnom/iscon contain True at column index where attr is nom/continous
        isnom = [(features.value_count(i) != 0) for i in range(features.cols)]
        iscon = [(features.value_count(i) == 0) for i in range(features.cols)]
        self.isnom, self.iscon = np.array(isnom), np.array(iscon)

        self.feats[self.feats==np.inf] = np.nan

    def calc_dists(self, feats, points):
        dists = np.zeros((feats.shape[0], points.shape[0]))  # distances of every instance (n) to each centroid (k)
        for i in range(points.shape[0]):
            diffs = self.calc_diffs(feats, points[i])
            # dists[:,i] = self.euclid(diffs)
            dists[:,i] = self.manhattan(diffs)
        return np.squeeze(dists)

    def calc_diffs(self, feats, point):
        diffs = feats-point  # differences btw features and point (centroid or silhouette point)
        diffs[np.isnan(diffs)] = 1  # all unknown values have distance of 1
        noms = diffs[:,self.isnom]
        noms[noms != 0] = 1  # if nom values are not equal, then dist is 1
        diffs[:,self.isnom] = noms
        return diffs

    def euclid(self, diffs):
        sq_diffs = np.square(diffs)  # squares all diffs
        return np.sum(sq_diffs,axis=1)**0.5  # returns array of dists to centroids for each instance

    def manhattan(self, diffs):
        return np.sum(abs(diffs), axis=1)

    def new_centroids(self, dists, cluster_inds):
        sse = 0
        for i in range(self.k):
            inds = np.squeeze(np.argwhere(cluster_inds == i))  # row indices of instances in cluster i
            self.cluster_list[i] = int(inds.size)
            self.sse_list[i] = np.sum(np.square(dists[:,i][inds]))  # adding the dists of each inst to centroid
            modes, means = self.find_centroid(inds, i)
            self.cents[i][self.isnom] = modes
            self.cents[i][self.iscon] = means
        self.SSE = np.sum(self.sse_list)

    def find_centroid(self, inds, i):
        # Nominal values: centroid is mode of column (ignoring ?'s)
        cluster_n = self.feats[:,self.isnom][inds]  # select nominal feats where rows are in this cluster
        # to ignore nan's for mode, set to random 1e6<int<2e6
        mask = np.isnan(cluster_n)
        c = np.count_nonzero(mask)
        cluster_n[mask] = np.random.randint(1e6,1e7,c)
        modes = np.squeeze(stats.mode(cluster_n)[0])
        modes[modes>=1e6] = np.nan  # edge case where all vals in col are nan

        # Continuous values: centroid is mean of column (ignoring ?'s)
        cluster_c = self.feats[:,self.iscon][inds]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            means = np.nanmean(cluster_c, axis=0)
        return modes, means

    def find_silhouette(self, cluster_inds):
        clusters = []
        for i in range(self.k):
            inds = np.squeeze(np.argwhere(cluster_inds == i))
            cluster = self.feats[inds]
            clusters.append(cluster)
        score = 0
        for i in range(self.k):
            a = self.find_a(clusters[i])
            b = self.find_b(clusters, clusters[i])
            mask = a>b
            maxes = np.zeros(a.size)
            maxes[mask] = a[mask]
            maxes[~mask] = b[~mask]
            score += np.sum((b - a)/maxes)
        return score/self.n

    def find_a(self, cluster):
        dists = self.calc_dists(cluster, cluster)
        sums = np.sum(dists, axis=1)
        a = sums/(sums.size-1)
        return a

    def find_b(self, clusters, cluster):
        dists = self.calc_dists(cluster, self.cents)
        inds_next = np.argpartition(dists,1)[:,1]
        b = np.zeros(cluster.shape[0])
        for i in range(cluster.shape[0]):
            next_cluster = clusters[inds_next[i]]
            point = np.array([cluster[i]])
            dists_next = self.calc_dists(next_cluster, point)
            sum_next = np.sum(dists_next)
            b_point = sum_next/next_cluster.shape[0]
            b[i] = b_point
        return b

    def print_centroids(self, features):
        s = ''
        for i in range(self.k):
            # s += '\tCentroid {} = '.format(i)
            for j in range(self.m):
                val = self.cents[i][j]
                # if self.isnom[j] and not np.isnan(val):
                    # sval = features.attr_value(j, val)
                if np.isnan(val):
                    sval = '?'
                else:
                    sval = '{:1.2f}'.format(val)

                if j == self.m-1:
                    s += '{}\n'.format(sval)
                else:
                    s += '{} '.format(sval)
        print(s)

    def print_inds(self, cluster_inds):
        print('Making assignments:')
        s = '\t'
        for i in range(self.n):
            index = '{:d}'.format(i)
            if index[-1] == '9':
                s += '{}={:d}\n\t'.format(index,cluster_inds[i])
            else:
                s += '{}={:d} '.format(index,cluster_inds[i])
        print(s)

    def print_clusters_info(self):
        s = ''
        for k in range(self.k):
            s += 'Cluster {}:\n\tinstances: {}, SSE: {:1.2f}\n'.format(k,
                int(self.cluster_list[k]), self.sse_list[k])
        print(s)
