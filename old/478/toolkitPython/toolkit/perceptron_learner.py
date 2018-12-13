from .supervised_learner import SupervisedLearner
from .matrix import Matrix
import random
import numpy as np


class PerceptronLearner(SupervisedLearner):

    def __init__(self):
        self.weights = np.zeros((0,0))
        self.bias = 1
        self.perceptrons = 0

    def train(self, features, labels):
        """
        Before you call this method, you need to divide your data
        into a feature matrix and a label matrix.
        :type features: Matrix
        :type labels: Matrix
        """

        c = 0.1  # learning rate
        num_scores = 5
        threshold = 0.003

        num_classes = labels.value_count(0)
        print("Number of classes:",num_classes)
        if num_classes == 2:
            # Perceptron only needs to be ran once
            self.perceptrons = 1
        else:
            # One perceptron for each class
            self.perceptrons = num_classes

        # Weights: 2d array where each row is the weights vector for each class
        self.weights = [[random.uniform(-0.1, 0.1) for i in range(features.cols+1)] for j in range(self.perceptrons)]

        for k in range(self.perceptrons):
            scores = []
            epoch = 0
            repeat = True
            while repeat:
                features.shuffle(labels)
                count_score = 0
                for i in range(features.rows):  # loop through rows
                    row = features.row(i)
                    if epoch == 0 and k == 0:
                        row.append(self.bias)

                    net = 0
                    output = 0
                    target = 0
                    for j in range(len(row)):  # loop through column values
                        net += row[j] * self.weights[k][j]
                    if net > 0:
                        output = 1

                    # For 3+ classes, the class of the current perceptron will be 1
                    # and all other classes will be 0.
                    label = labels.get(i,0)
                    if self.perceptrons == 1:
                        target = label
                    elif label == k:
                        target = 1
                    elif label != k:
                        target = 0

                    if output == target:
                        count_score += 1

                    for j in range(len(row)):
                        self.weights[k][j] += c*(target-output) * row[j]

                # Calculate improvement in accuracy over last 5 epochs
                score = count_score / features.rows
                # print(score)
                scores.append(score)
                if epoch >= num_scores:
                    diff_sum = 0
                    for i in range(num_scores-1):
                        diff_sum += abs(scores[1+epoch-num_scores+i] - scores[epoch-num_scores+i])
                    mean_diff = diff_sum / (num_scores-1)
                    if mean_diff < threshold:
                        repeat = False
                        continue

                epoch += 1



            print("Number of epochs:", epoch)

    def predict(self, features, labels):
        """
        A feature vector goes in. A label vector comes out. (Some supervised
        learning algorithms only support one-dimensional label vectors. Some
        support multi-dimensional label vectors.)
        :type features: [float]
        :type labels: [float]
        """

        guess = False
        output = 0
        net_high = 0
        for k in range(self.perceptrons):
            net = 0
            for i in range(len(features)):
                net += features[i] * self.weights[k][i]
            if self.perceptrons == 1:
                if net > 0:
                    output = 1
                else:
                    output = 0
            else:
                if net > net_high:
                    net_high = net
                    output = k

        if len(labels) == 0:
            labels.append(output)
        else:
            labels[0] = output
