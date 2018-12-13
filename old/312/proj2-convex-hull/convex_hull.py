#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time



class ConvexHullSolver:
    def __init__( self, display ):
        self.points = []
        self.gui_display = display
        self.hullL = None
        self.hullR = None
        self.top_tangent = True
        self.l_index = 0

    def compute_hull( self, unsorted_points ):
        assert( type(unsorted_points) == list and type(unsorted_points[0]) == QPointF )

        n = len(unsorted_points)
        print( 'Computing Hull for set of {} points'.format(n) )

        t1 = time.time()
        # TODO: SORT THE POINTS BY INCREASING X-VALUE
        self.points = sorted(unsorted_points, key=QPointF.x)
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

        t3 = time.time()
        # TODO: COMPUTE THE CONVEX HULL USING DIVIDE AND CONQUER
        convex_hull = self.makeHull(0, len(self.points)-1)
        t4 = time.time()


        USE_DUMMY = False
        if USE_DUMMY:
            # this is a dummy polygon of the first 3 unsorted points
            polygon = [QLineF(unsorted_points[i],unsorted_points[(i+1)%3]) for i in range(3)]

            # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
            # object can be created with two QPointF objects corresponding to the endpoints
            assert( type(polygon) == list and type(polygon[0]) == QLineF )
            self.gui_display.addLines( polygon, (255,0,0) )
        else:
            # TODO: PASS THE CONVEX HULL LINES BACK TO THE GUI FOR DISPLAY
            polygon = [QLineF(self.points[convex_hull[i]],
                                self.points[convex_hull[(i+1)%len(convex_hull)]]) for i in range(len(convex_hull))]
            assert( type(polygon) == list and type(polygon[0]) == QLineF )
            self.gui_display.addLines( polygon, (255,0,0) )

        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
        self.gui_display.displayStatusText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

        # refresh the gui display
        self.gui_display.update()

    # This recursive function divides self.points into the smallest hulls possible
    # (size 2 or size 3), sorts the hulls' points into clockwise order, then combines
    # each hull until the complete convex hull is returned.
    # L, R are indices of points, where L is the smaller index and R is the greater
    # First indices passed in are first index and last index of self.points
    def makeHull(self, L, R):
        if R-L > 2: # Base case is a set of 3 or 2 points
            hullL = self.makeHull(L, (L+R)//2)
            hullR = self.makeHull((L+R)//2+1, R)
            return self.combineHulls(hullL, hullR)
        else:
            return self.sortClockwise(L, R)

    # Takes in two hulls of points and returns one hull for the entire group of points.
    # The hulls are lists of indices for self.points, which represent point 1, point 2,
    # etc., of the entire plot of points, sorted from smallest to largest x value.
    def combineHulls(self, hullL, hullR):
        self.hullL = hullL
        self.hullR = hullR
        Lt, Rt, Lb, Rb = self.findTangents()
        L = 0
        merged_hull = []
        for L in range(Lt):
            merged_hull.append(self.hullL[L])
        merged_hull.append(self.hullL[Lt])
        R = Rt
        if Rb == 0:
            for R in range(R, len(hullR)):
                merged_hull.append(self.hullR[R])
        elif Rt > Rb:
            for R in range(R, Rb, -1):
                merged_hull.append(self.hullR[R])
        elif Rt < Rb:
            for R in range(R, Rb):
                merged_hull.append(self.hullR[R])
        merged_hull.append(self.hullR[Rb])
        L = Lb
        if L != 0:
            for L in range(L, len(hullL)):
                merged_hull.append(self.hullL[L])

        return merged_hull

    # Finds the top and bottom tangents of hullL and hullR and returns the four hull indices.
    def findTangents(self):
        self.l_index = 0
        for i in range(len(self.hullL)):
            pl = self.points[self.hullL[i]]
            i2 = i+1
            if i2 == len(self.hullL):
                i2 = 0
            pl2 = self.points[self.hullL[i2]]
            if pl.x() > pl2.x():
                self.l_index = i
                break
        l = self.l_index
        r = 0
        pivot = ['r', 0]
        prev_pivot = pivot
        self.top_tangent = True
        while self.top_tangent == True:
            if pivot[0] == 'r':
                prev_pivot = pivot
            l, r, pivot = self.findTopTangent(l, r, pivot, prev_pivot)

        Lt, Rt = l, r
        l = self.l_index
        r = 0
        pivot = ['r', r]
        while self.top_tangent == False:
            if pivot[0] == 'r':
                prev_pivot = pivot
            l, r, pivot = self.findBotTangent(l, r, pivot, prev_pivot)

        Lb, Rb = l, r
        return Lt, Rt, Lb,  Rb

    # Takes in an index of both a point on the left and a point on the right hull,
    # along with the current pivot point (which is one of the two given indices) and the last pivot.
    # The algorithm is the same for finding the top or the bottom tangent, but with scanning
    # the points of the hulls in opposite directions and with flipped slope conditions.
    # The initial pivot point is leftmost point of the right hull.
    def findTopTangent(self, l, r, pivot, prev_pivot):
        pl  = self.points[self.hullL[l]]
        pr  = self.points[self.hullR[r]]
        slope1 = (pr.y() - pl.y()) / (pr.x() - pl.x())
        if pivot[0] == 'r':
            l2 = l-1
            if l2 == -1:
                l2 = len(self.hullL)-1
            pl2 = self.points[self.hullL[l2]]
            slope2 = (pr.y() - pl2.y()) / (pr.x() - pl2.x())
            if slope2 < slope1:
                return l2, r, pivot
            else:
                pivot = ['l',l]
                return l, r, pivot
        elif pivot[0] == 'l':
            r2 = r+1
            if r2 == len(self.hullR):
                r2 = 0
            pr2 = self.points[self.hullR[r2]]
            slope2 = (pr2.y() - pl.y()) / (pr2.x() - pl.x())
            if slope2 > slope1:
                return l, r2, pivot
            else:
                if prev_pivot == ['r', r]:
                    self.top_tangent = False
                pivot = ['r',r]
                return l, r, pivot

    def findBotTangent(self, l, r, pivot, prev_pivot):
        pl  = self.points[self.hullL[l]]
        pr  = self.points[self.hullR[r]]
        slope1 = (pl.y() - pr.y()) / (pl.x() - pr.x())
        if pivot[0] == 'r':
            l2 = l+1
            if l2 == len(self.hullL):
                l2 = 0
            pl2 = self.points[self.hullL[l2]]
            slope2 = (pr.y() - pl2.y()) / (pr.x() - pl2.x())
            if slope2 > slope1:
                return l2, r, pivot
            else:
                pivot = ['l',l]
                return l, r, pivot
        elif pivot[0] == 'l':
            r2 = r-1
            if r2 == -1:
                r2 = len(self.hullR)-1
            pr2 = self.points[self.hullR[r2]]
            slope2 = (pr2.y() - pl.y()) / (pr2.x() - pl.x())
            if slope2 < slope1:
                return l, r2, pivot
            else:
                if prev_pivot == ['r', r]:
                    self.top_tangent = True
                pivot = ['r',r]
                return l, r, pivot

    # Sorts 2 or 3 indices of points into their clockwise order, and returns it as a hull (list of self.points indices).
    def sortClockwise(self, L, R):
        if R-L == 1:
            return [L, R]
        else:
            i2 = R-1
            i3 = R
            p1 = self.points[L]
            p2 = self.points[i2]
            p3 = self.points[i3]
            slope12 = (p1.y() - p2.y()) / (p1.x() - p2.x())
            slope13 = (p1.y() - p3.y()) / (p1.x() - p3.x())
            if slope12 > slope13:
                return [L, i2, i3]
            else:
                return [L, i3, i2]
