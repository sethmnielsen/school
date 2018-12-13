from .supervised_learner import SupervisedLearner
import random
import numpy as np
from math import exp
from .matrix import Matrix
from copy import deepcopy

# command to run: python3 -m toolkit.manager -L backprop -A datasets/iris.arff -E training
class BackpropLearner(SupervisedLearner):
    def __init__(self):
        self.in_weights = np.zeros((0,0))
        self.hid_weights = np.zeros((0,0))

        self.in_nodes = 0
        self.hid_nodes = 0
        self.out_nodes = 0

        self.hid_deltas = np.zeros((0,0))  # Previous hidden weight deltas
        self.in_deltas = np.zeros((0,0))   # Previous input weight deltas

        self.inputs = []
        self.hid_outputs = []
        self.c = 1 # learning rate
        self.bias = .5

        self.m = 2 # multiplier for number of hidden nodes
        self.alpha = 0.4 # momentum

    def train(self, features, labels):
        '''
            Count number of inputs, and set number of hidden nodes to be a multiple
            of the number of inputs. Only one hidden layer, and one output layer. Add
            bias to each hidden and output node.
            1) Find nets using inputs and weights (include bias input+weight)
            2) Find outputs of nodes using 1/(1+exp(-net))
            3) Use outputs as inputs for hidden layer
            4) Repeat for output node
            5) Calculate delta erro for output node: d = (t-O) * O(1-O)
            6) Update weights for hidden nodes: wij = C*Oi*dj
            7) Calculate delta errors for hidden nodes: dj = Oj*(1-Oj)*Ok*wjk (k is output node, j is current hid node)
            8) Update weights for input nodes: wij = C*Oi*dj
            9) Repeat for next training pattern using all the updated weights

            Include:
             - small random initial weights (0 mean)
             - weight update
             - stopping criterion
             - training set randomization at each epoch
             - momentum term option
        '''
        self.in_nodes = features.cols
        # self.hid_nodes = self.in_nodes * self.m
        self.hid_nodes = 64
        self.out_nodes = labels.value_count(0)

        # self.in_weights =  [[random.uniform(-0.1, 0.1) for j in range(self.hid_nodes)] for i in range(self.in_nodes+1)]
        # self.hid_weights = [[random.uniform(-0.1, 0.1) for j in range(self.out_nodes)] for i in range(self.hid_nodes+1)]
        self.in_weights =  np.array([[0.1 for j in range(self.hid_nodes)] for i in range(self.in_nodes+1)])
        self.hid_weights = np.array([[0.1 for j in range(self.out_nodes)] for i in range(self.hid_nodes+1)])

        print(self.in_weights)

        # Add bias input to each training pattern
        for row in features.data:
            row.append(self.bias)

        # Split validation set off of training set
        features.shuffle(labels)
        vs_percent = 1/3  # 1/3 of 75% is 25% of total dataset
        vs_size = int(vs_percent * features.rows)
        train_size = features.rows - vs_size

        train_features = Matrix(features, 0, 0, train_size, features.cols+1)
        train_labels = Matrix(labels, 0, 0, train_size, 1)

        vs_features = Matrix(features, train_size, 0, vs_size, features.cols+1)
        vs_labels = Matrix(labels, train_size, 0, vs_size, 1)

        # For stopping criterion
        best_in_weights = self.in_weights
        best_hid_weights = self.hid_weights
        best_mse = 1000
        best_acc = 0
        best_epoch = 0
        epoch_window = 5

        epoch = 0
        repeat = True
        while repeat:  # epoch loop
            epoch += 1
            train_features.shuffle(train_labels)
            for k in range(train_features.rows):  # training set loop; skip over validation set
                self.inputs = train_features.row(k)
                outputs = self.find_outputs(self.inputs)

                t = int(train_labels.get(k,0))  # target value
                targs = [0] * self.out_nodes    # output node of the label class has t = 1.0, and t = 0 for all other output nodes
                targs[t] = 1.0
                out_errs, hid_errs = self.find_errs(targs, outputs)

                self.update_weights(out_errs, hid_errs)

            # Calculate MSE on validation set
            mse, acc = self.find_mse(vs_features, vs_labels)
            if mse < best_mse:
                train_mse, train_acc = self.find_mse(train_features, train_labels)
                best_mse = mse
                best_acc = acc
                best_in_weights = deepcopy(self.in_weights)
                best_hid_weights = deepcopy(self.hid_weights)
                best_epoch = epoch
            else:
                if epoch - best_epoch >= epoch_window:
                    self.in_weights = best_in_weights
                    self.hid_weights = best_hid_weights
                    print('\nLast epoch:', best_epoch)
                    print('Train MSE:', train_mse)
                    print('VS MSE: {}'.format(best_mse))
                    repeat = False

        # print('In weights:', self.in_weights)
        # print('Hid weights:', self.hid_weights)

    def find_mse(self, features, labels):
        se_sum = 0
        score = 0
        for k in range(features.rows):
            inputs = features.row(k)
            outputs = self.find_outputs(inputs)

            high = np.max(outputs)
            pred = list(outputs).index(high)
            t = int(labels.get(k,0))
            targs = [0] * self.out_nodes
            targs[t] = 1.0

            se_sum += self.squared_error(targs, outputs)
            if pred == t:
                score += 1

        mse = se_sum / features.rows
        accuracy = score / features.rows
        return mse, accuracy

    def find_outputs(self, inputs):
        self.hid_outputs = [0] * (self.hid_nodes+1)
        for j in range(self.hid_nodes):  # loop through hid nodes
            net = 0
            for i in range(len(inputs)):  # loop through weights & values of input nodes
                x = inputs[i]
                w = self.in_weights[i][j]
                net += x*w
            self.hid_outputs[j] = self.sig(net)
        self.hid_outputs[-1] = self.bias  # bias hidden node
        outputs = np.zeros(self.out_nodes)
        for j in range(self.out_nodes):
            outputs[j] = self.this_output(j)
        return outputs

    def this_output(self, j):
        net = 0
        for i in range(self.hid_nodes+1):  # loop through weights & values of hid nodes
            x = self.hid_outputs[i]
            w = self.hid_weights[i][j]
            net += x*w
        return self.sig(net)

    def find_errs(self, targs, outputs):
        out_errs = [0]*self.out_nodes
        for j in range(self.out_nodes):
            z = outputs[j]
            error = targs[j]-z
            out_errs[j] = error*self.fp(z)

        hid_errs = [0]*self.hid_nodes
        for j in range(self.hid_nodes):
            z = self.hid_outputs[j]
            err_sum = 0
            for k in range(self.out_nodes):
                err_sum += out_errs[k]*self.hid_weights[j][k]
            hid_errs[j] = err_sum*self.fp(z)
        return out_errs, hid_errs

    def update_weights(self, out_errs, hid_errs):
        if len(self.hid_deltas) == 0:
            self.hid_deltas = np.zeros((len(self.hid_outputs),len(out_errs)))
            self.in_deltas  = np.zeros((len(self.inputs),len(hid_errs)))
        self.update_layer(self.hid_weights, self.hid_deltas, out_errs, self.hid_outputs)
        self.update_layer(self.in_weights, self.in_deltas, hid_errs, self.inputs)

    def update_layer(self, weights, delta_weights, errs, outs):
        for j in range(len(errs)):
            for i in range(len(outs)):
                del_w = self.c*outs[i]*errs[j] + self.alpha*delta_weights[i][j]
                delta_weights[i][j] = del_w
                weights[i][j] = weights[i][j] + del_w

    def sig(self, net):
        return 1/(1+exp(-net))

    def fp(self, z):
        return z*(1-z)

    def squared_error(self, targs, outputs):
        sq_error_sum = 0
        for i in range(self.out_nodes):
            sq_error_sum += (targs[i] - outputs[i])**2
        return sq_error_sum

    def predict(self, features, labels):
        """
        A feature vector goes in. A label vector comes out. (Some supervised
        learning algorithms only support one-dimensional label vectors. Some
        support multi-dimensional label vectors.)
        :type features: [float]
        :type labels: [float]
        """
        outputs = self.find_outputs(features)
        high = np.max(outputs)
        pred = list(outputs).index(high)

        if len(labels) == 0:
            labels.append(pred)
        else:
            labels[0] = pred
