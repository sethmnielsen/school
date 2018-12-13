#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
import math

class GeneSequencing:

    class Element:
        def __init__(self):
            self.cost = 0
            self.parent = [0, 0]

    def __init__( self ):
        pass

    def align_all( self, sequences, banded, align_length ):
        prev_ij = []
        results = []
        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):
                self.align_i = ''
                self.align_j = ''
                cost = 0
                calc = True
                for k in range(len(prev_ij)):  # check if both seqs have been visited already
                    if prev_ij[k] == [j,i]:
                        calc = False
                if calc:  # proceed with calculation
                    prev_ij.append([i,j])  # store this combo of sequences
                    if i == j:  # sequences are the same
                        l = align_length
                        if align_length > len(sequences[i]):
                            l = len(sequences[i])
                        cost = -3 * l
                        self.align_i = sequences[i]
                        self.align_j = sequences[j]
                    else:
                        self.seqi = sequences[i][:align_length]
                        self.seqj = sequences[j][:align_length]
                        if banded and abs(len(self.seqi) - len(self.seqj)) > 3:  # sequences size discrepancy too large
                            cost = math.inf
                            self.align_i = 'No Alignment Possible'
                            self.align_j = 'No Alignment Possible'
                        else:
                            print('Create table on ({},{})'.format(i,j))
                            self.create_table(banded)
                            print('Finding cost on ({},{})'.format(i,j))
                            cost = self.find_cost(banded)
                            print('Got cost')
                s = {'align_cost':cost,
                     'seqi_first100':'{}{}'.format(self.align_i[:100], ',BANDED' if banded else ''),
                     'seqj_first100':'{}{}'.format(self.align_j[:100], ',BANDED' if banded else '')}
                if i == 3-1 and j == 10-1:
                    print('seqi_alignment:')
                    print(self.align_i[:100])
                    print('seqj_alignment:')
                    print(self.align_j[:100])
                jresults.append(s)
            results.append(jresults)
        return results

    def create_table(self, banded):
        sizei = len(self.seqi) + 1
        sizej = len(self.seqj) + 1

        self.table = np.zeros((sizei,sizej)).tolist()
        for i in range(sizei):
            for j in range(sizej):
                if banded and abs(i-j) > 3:  # outside of band, no need to create Element object
                    continue
                self.table[i][j] = self.Element()

        if banded:
            sizei = 4
            sizej = 4

        for i in range(sizei):  # initialize first row and column costs
            self.table[i][0].cost = i*5
            self.table[i][0].parent = [-1,0]
            for j in range(sizej):
                self.table[0][j].cost = j*5
                self.table[0][j].parent = [0,-1]

    def find_cost(self, banded):
        # dict for pair combos
        c = {'match': -3, 'sub': 1, 'indel': 5}

        mincost = 0
        costs = [0]*3
        for i in range(1,len(self.seqi)+1):
            for j in range(1,len(self.seqj)+1):
                if banded and abs(i-j) > 3:  # outside of band
                    continue
                try:
                    costs[0] = self.table[i-1][j].cost + c['indel']  # from above
                except:
                    costs[0] = math.inf
                try:
                    costs[1] = self.table[i][j-1].cost + c['indel']  # from left
                except:
                    costs[1] = math.inf

                costs[2] = self.table[i-1][j-1].cost  # diagonal
                if self.seqi[i-1] == self.seqj[j-1]:
                    costs[2] += c['match']
                else:
                    costs[2] += c['sub']
                mincost = costs[2]
                minindex = 2
                for k in range(2):
                    if costs[k] < mincost:
                        mincost = costs[k]
                        minindex = k
                parent = [-1, -1]
                if minindex == 0:
                    parent = [-1, 0]
                elif minindex == 1:
                    parent = [0, -1]
                self.table[i][j].parent = parent
                self.table[i][j].cost = mincost

        print('Aligning')
        self.align()
        print('Aligned')
        return self.table[-1][-1].cost

    def align(self):
        i = len(self.seqi)
        j = len(self.seqj)
        self.seqi = '-' + self.seqi
        self.seqj = '-' + self.seqj
        self.align_i = self.seqi[-1]
        self.align_j = self.seqj[-1]
        p = self.table[i][j].parent  # parent = [-i, -j]
        p_pos = [i + p[0], j + p[1]]
        while p_pos != [0,0]:
            i += p[0]
            j += p[1]
            add_i = self.seqi[i]
            add_j = self.seqj[j]
            if p[0] == 0:
                add_i = '-'
            elif p[1] == 0:
                add_j = '-'
            self.align_i = add_i + self.align_i
            self.align_j = add_j + self.align_j
            p = self.table[i][j].parent
            p_pos = [i + p[0], j + p[1]]

    def print_table(self, seqi, seqj):
        n = [['', ''], ['']]
        for i in range(len(seqi)):
            n.append([seqi[i]])
        for j in range(len(seqj)):
            n[0].append(seqj[j])

        for i in range(len(seqi)+1):
            for j in range(len(seqj)+1):
                n[i+1].append(self.table[i][j].parent)

        print('Cost table:')
        s = '[\n[{:>8}'.format('')
        for j in range(1,len(n[0])):
            s += ', {:>8}'.format(n[0][j])
        s += '],\n'
        for i in range(1,len(n)):
            s += '[{:>8}'.format(n[i][0])
            for j in range(1,len(n[0])):
                s += ', {:>8}'.format(str(n[i][j]))
            s += '],\n'
        s += ']'
        print(s)
