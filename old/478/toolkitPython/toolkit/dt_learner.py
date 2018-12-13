from .supervised_learner import SupervisedLearner
import random
from collections import Counter
import numpy as np
from math import exp
from .matrix import Matrix
from IPython.core.debugger import Pdb

class DTLearner(SupervisedLearner):
    class Node:
        def __init__(self, attr=None):
            self.data = []  # data contained under this node (answer for leaf)
            self.attr = attr  # attribute that this node splits on

        def to_array(self):
            if self.attr == -1:
                return self.data
            vals = np.zeros(0, dtype=int)
            for data in self.data:
                vals = np.append(vals,data.to_array())
            return vals

    def train(self, features, labels):
        '''
        1. Find total entropy
        2. Find entropy and info gain of each attribute
        3. Split on attribute with highest info gain (new node)
        4. Create new matrices where each one has only one value of that attribute
        5. Repeat
        5. Stop when only one output class left
        '''
        self.nodes = 0
        self.levels = 0
        self.depth = 0
        self.num_classes = labels.value_count(0)

        # Split validation set off of training set
        features.shuffle(labels)
        vs_percent = 1/3 # 1/3 of 75% is 25% of total dataset
        vs_size = int(vs_percent * features.rows)
        train_size = features.rows - vs_size

        self.vs_features = Matrix(features, train_size, 0, vs_size, features.cols+1)
        self.vs_labels = Matrix(labels, train_size, 0, vs_size, 1)

        features = Matrix(features, 0, 0, train_size, features.cols+1)
        labels = Matrix(labels, 0, 0, train_size, 1)

        data = self.convert_numpy(features, labels)
        vs_data = self.convert_numpy(self.vs_features, self.vs_labels)

        split_list = [None] * features.cols
        self.tree = self.split(data, split_list)

        if len(vs_data) > 0:
            self.prune(self.tree, vs_data)

        print(np.bincount(self.tree.to_array()))

        self.count_nodes(self.tree)

    def prune(self, node, vs_data):
        if node.attr == -1:
            return
        else:
            for n in node.data:
                self.prune(n, vs_data)

            attr_save = node.attr
            pre_accuracy = self.measure_accuracy(self.vs_features, self.vs_labels)
            node.attr = -1
            post_accuracy = self.measure_accuracy(self.vs_features, self.vs_labels)
            node.attr = attr_save
            if post_accuracy >= pre_accuracy:
                data_array = node.to_array()
                node.attr = -1
                node.data = Counter(data_array).most_common(1)[0][0]

    def count_nodes(self, node):
        self.nodes += 1
        self.levels += 1
        if self.levels > self.depth:
            self.depth = self.levels
        if node.attr == -1:
            return
        for n in node.data:
            self.count_nodes(n)
            self.levels -= 1

    def convert_numpy(self, features, labels):
        data = np.zeros((features.rows,features.cols+1))
        for i in range(features.cols):
            col = np.asarray(features.col(i))
            col[col == np.inf] = -1
            data[:,i] = col
        data[:,-1] = labels.col(0)
        data = data.astype(int)
        if np.any(data == -1):
            data = self.fill_missing_vals(data, features)
        return data

    def fill_missing_vals(self, data, features):
        self.gen_features = np.zeros((self.num_classes,len(data[0])),dtype=int)
        filled_data = np.zeros((0, len(data[0])),dtype=int)
        for i in range(self.num_classes):
            class_data = np.zeros((0,len(data[0])),dtype=int)
            for j in range(len(data)):  # rows
                row = data[j]
                if row[-1] == i:
                    class_data = np.vstack((class_data, data[j]))
            for k in range(len(data[0])):  # cols
                com_vals = Counter(class_data[:,k]).most_common(2)
                gen_val = com_vals[0][0]
                if gen_val == -1:
                    gen_val = com_vals[1][0]
                col = class_data[:,k]
                col[col == -1] = gen_val
                self.gen_features[i][k] = gen_val

            filled_data = np.vstack((filled_data, class_data))
        return filled_data

    def split(self, data, split_list):
        reduced_data = np.zeros((0,len(data[0])),dtype=int)
        all_none = True
        for i in range(len(split_list)):  # i is which feature we split on
            if split_list[i] is not None:
                all_none = False
                for j in range(len(data)):  # j is row of data
                    row = data[j]
                    if row[i] == split_list[i]:
                        reduced_data = np.vstack((reduced_data, data[j]))
        if all_none:
            reduced_data = data

        num_labels = np.trim_zeros(np.bincount(reduced_data[:,-1]))
        if len(num_labels) == 1:
            return self.make_leaf(reduced_data[:,-1])

        ents = np.zeros(len(data[0])-1)
        for i in range(len(ents)):
            ents[i] = self.entropy_A(reduced_data[:,i], reduced_data[:,-1])

        f = np.argmin(ents)  # index of feature with min entropy
        feat_count = np.bincount(reduced_data[:,f])  # Everything in the f column
        new_node = self.Node(f)
        for i in range(len(feat_count)):
            if feat_count[i] == 0:
                return self.make_leaf(reduced_data[:,-1])
            split_list_new = [None] * (len(data[0])-1)
            split_list_new[f] = i
            new_node.data.append(self.split(reduced_data, split_list_new))

        return new_node

    def entropy_A(self, feature, labels):
        ent_sum = 0
        feat_count = np.bincount(feature)
        num_vals = len(feat_count)
        total_ent = 0
        for i in range(num_vals):
            val_count = feat_count[i]
            if val_count == 0:
                continue
            val_set = np.zeros((0,2),dtype=int)
            for j in range(len(feature)):
                if feature[j] == i:
                    val_set = np.vstack((val_set,[int(i),labels[j]]))
            e = (val_count/len(feature))*self.entropy(val_set, val_count)
            total_ent += e

        return total_ent

    def entropy(self, val_set, val_count):
        label_count = np.bincount(val_set[:,1])
        ent_sum = 0
        for i in range(len(label_count)):
            if label_count[i] == 0:
                continue
            p = label_count[i]/val_count
            ent = p*np.log2(p)
            ent_sum += -ent
        return ent_sum

    def make_leaf(self, col):
        leaf = self.Node(-1)
        leaf.data = Counter(col).most_common(1)[0][0]
        return leaf

    def predict(self, features, labels):
        """
        A feature vector goes in. A label vector comes out. (Some supervised
        learning algorithms only support one-dimensional label vectors. Some
        support multi-dimensional label vectors.)
        :type features: [float]
        :type labels: [float]
        """
        features = np.asarray(features)
        if np.any(features == np.inf):
            for i in range(len(features)):
                if features[i] == np.inf:
                    features[i] = self.gen_features[0][i]
        pred = self.traverse_tree(features, self.tree)

        if len(labels) == 0:
            labels.append(pred)
        else:
            labels[0] = pred

    def traverse_tree(self, features, node):
        if node.attr == -1:
            # data_array = node.to_array()
            if isinstance(node.data, np.int64):
                major_class = node.data
            else:
                pruned_array = np.zeros(0, dtype=int)
                for n in node.data:
                    pruned_array = np.append(pruned_array, n.to_array())
                    major_class = Counter(pruned_array).most_common(1)[0][0]
            return major_class

        index = int(features[node.attr])
        if index >= len(node.data):
            return Counter(node.to_array()).most_common(1)[0][0]

        return self.traverse_tree(features, node.data[index])
