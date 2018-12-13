#!/usr/bin/python3
from CS312Graph import *
import time
from copy import deepcopy
from unsortedarray import Uarray
from minheap import MinHeap


class NetworkRoutingSolver:
    def __init__( self, display ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        path_edges = []
        total_length = 0

        # Path is constructed starting at target and using the 'prev' edges to
        # work back to the source.
        node = self.network.nodes[self.dest]
        edge = node.prev
        while edge is not None:
            path_edges.append( (edge.dest.loc, edge.src.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length

            edge = edge.src.prev

        if total_length == 0:
            total_length = float('inf')
        return {'cost':total_length, 'path':path_edges}



    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex

        t1 = time.time()
        self.network.nodes[self.source].dist = 0
        H = None
        if use_heap:
            H = MinHeap(self.network.nodes)
        else:
            H = Uarray(self.network.nodes)

        while len(H.V) > 0:
            u = H.delete_min()
            for e in u.neighbors:
                v = e.dest
                if v.dist > u.dist + e.length:
                    v.dist = u.dist + e.length
                    v.prev = e  # 'prev' is the edge leading to the node
                    H.decrease_key(v)

        t2 = time.time()

        return (t2-t1)
