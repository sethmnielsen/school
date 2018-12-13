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
from TSPClasses import *
from StateNode import StateNode
from heapq import heappush, heappop



class TSPSolver:
    def __init__( self, gui_view ):
        self._scenario = None

    def setupWithScenario( self, scenario ):
        self._scenario = scenario

    def defaultRandomTour( self, start_time, time_allowance=60.0 ):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        while not foundTour:
            # create a random permutation
            perm = np.random.permutation( ncities )

            route = []

            # Now build the route using the random permutation
            for i in range( ncities ):
                route.append( cities[ perm[i] ] )

            bssf = TSPSolution(route)
            count += 1

            if bssf.costOfRoute() < np.inf:
                # Found a valid route
                foundTour = True

        results['cost'] = bssf.costOfRoute()
        results['time'] = time.time() - start_time
        results['count'] = count
        results['soln'] = bssf

        return results

    def greedy( self, start_time, time_allowance=60.0 ):
        pass

    def branchAndBound( self, start_time, time_allowance=60.0 ):
        start_time = time.time()
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False

        random_result = self.defaultRandomTour(time.time())
        bssf = random_result['cost']
        bssf_soln = random_result['soln']

        print('Initial BSSF:',bssf)

        root = StateNode(root=True, cities=cities)
        heap = []
        heappush(heap, (root.keyvalue, root))
        max_q = 1
        bssf_count = 0
        total_nodes = 1
        prune_count = 0

        while len(heap) > 0:
            if time.time() - start_time > time_allowance:
                break

            if len(heap) > max_q:
                max_q = len(heap)

            node = heappop(heap)[1]
            if node.lb < bssf:
                if node.cities_left.size > 0:
                    children = node.expand()
                    total_nodes += children.size
                    for child in children:
                        if child.lb < bssf:
                            heappush(heap, (child.keyvalue, child))
                        else:
                            prune_count += 1
                else:
                    route = node.path
                    tour = TSPSolution(route)
                    tour_cost = tour.costOfRoute()
                    if tour_cost < bssf:
                        bssf = tour_cost
                        bssf_soln = tour
                        bssf_count += 1

            else:
                prune_count += 1

        results['time'] = time.time() - start_time
        results['cost'] = bssf_soln.costOfRoute()
        results['max_q'] = max_q
        results['count'] = bssf_count
        results['states'] = total_nodes
        results['pruned'] = prune_count
        results['soln'] = bssf_soln

        return results

    def fancy( self, start_time, time_allowance=60.0 ):
        pass
