from .supervised_learner import SupervisedLearner
import random
import numpy as np
from collections import Counter
from .matrix import Matrix
from IPython.core.debugger import Pdb

np.set_printoptions(precision=2,suppress=True)

class InstanceBasedLearner(SupervisedLearner):
    def __init__(self):
        self.weighted = False
        self.regression = False  # continuous output
        self.k = 3
        self.ignore = np.array([3,4,5,6,8,11,12,13,14])
        random.seed(0)

    def train(self, features, labels):
        self.num_classes = labels.value_count(0)
        if self.num_classes == 0:  # continuous values
            self.regression = True

        size = features.rows
        if size > 2000:
            size = 2000
        s = random.sample(range(features.rows), size)  # set of random row indices for reducing dataset
        self.features = features
        self.f = self.convert_numpy(features, s)
        self.l = self.convert_numpy(labels, s)


    def convert_numpy(self, features, s):
        data = np.zeros((len(s),features.cols))
        for i in range(len(s)):
            data[i] = np.array(features.row(s[i]))
        return data

    def predict(self, features, labels):
        """
        A feature vector goes in. A label vector comes out. (Some supervised
        learning algorithms only support one-dimensional label vectors. Some
        support multi-dimensional label vectors.)
        :type features: [float]
        :type labels: [float]
        """
        k = self.k
        dists = self.calc_dists(features)
        knn = np.argpartition(dists, k)[:k]  # returns list of k nearest neighbors

        if self.regression:  # continuous output
            if self.weighted:
                wf_sum = 0
                w_sum = 0
                for i in range(k):
                    w = 1/dists[knn[i]]**2
                    wf_sum += w*self.labels[knn[i]]
                    w_sum += w
                pred = wf_sum / w_sum
            else:
                raw_sum = 0
                for i in range(k):
                    raw_sum += self.l[knn[i]]
                avg = raw_sum / k
                pred = avg
        else:  # nominal output
            if self.weighted:
                votes = [0] * self.num_classes
                for i in range(self.num_classes):
                    for j in range(k):
                        if self.l[knn[j]] == i:
                            votes[i] += 1/dists[knn[j]]**2
                pred = np.argmax(votes)
            else:
                votes = [0] * k
                for i in range(k):
                    votes[i] = int(self.l[knn[i]])
                pred = Counter(votes).most_common(1)[0][0]


        if len(labels) == 0:
            labels.append(pred)
        else:
            labels[0] = pred

    def calc_dists(self, p):
        dists = np.zeros(0)
        for row in self.f:
            sq_sum = 0
            for i in range(len(row)):
                if np.any(self.ignore == i):
                    continue
                if row[i] == np.inf or p[i] == np.inf:
                    sq_sum += 1.
                elif self.features.value_count(i) == 0:
                    sq_sum += (row[i]-p[i])**2
                else:
                    sq_sum += self.vdm(i,row[i],p[i])**2
            d = sq_sum**0.5
            dists = np.append(dists, d)
        return dists

    def vdm(self, a, x, y):
        sq_sum = 0
        for i in range(self.num_classes):
            naxc = ((self.f[:,a] == x) & (self.l[:,0] == i)).sum()
            nax = (self.f[:,a] == x).sum()
            nayc = ((self.f[:,a] == y) & (self.l[:,0] == i)).sum()
            nay = (self.f[:,a] == y).sum()
            sq_sum += (naxc/nax - nayc/nay)**2
        return sq_sum
