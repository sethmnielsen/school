'''
For the poses and measurements included in the .mat file below, use the occupancy grid 
mapping techniques of chapter 9 (table 9.1 and 9.2) to create a map of the environment. 
You can assume the environment is well represented by a 100 m by 100 m grid where cells are 1 m square.

The state_meas_data.mat file includes three variables:

  1) X: state vector holding (x, y, theta) at each time step
  2) z: measurement vector holding (range, bearing) for nine laser range finder measurements 
     at each time step. NaN is reported if a "hit" is not detected.
  3) thk: vector of nine range finder pointing angles ranging between -pi/2 (-90 deg) and 
     pi/2 (90 deg). Pointing angles are equally spaced at pi/8 rad (22.5 deg) of separation. 

Use the following parameters for your inverse range sensor model: alpha = 1 m, beta = 5 deg, z_max = 150 m.

Use p(m_i)  = occupied be 0.6 to 0.7 if a "hit" is detected and 0.3 to 0.4 for p(m_i) = 
occupied if a "hit" is not detected for a particular cell.
'''

import sys
import time
import numpy as np

from PyQt5.QtCore import Qt
from pyqtgraph.Qt import QtCore, QtGui, Qt
import pyqtgraph as pg

class TurtleApp(pg.GraphicsObject):
    def __init__(self, pose, radius):
        pg.GraphicsObject.__init__(self)
        self.pose = QtCore.QPointF(*pose[:2])
        self.R = radius 
        pt = pose[:2] + np.array([np.cos(pose[2]), np.sin(pose[2])]) * self.R
        self.pt = QtCore.QPointF(*(pose[:2] + pt))
        self.generatePicture()

    def setPose(self, pose):
        self.pose.setX(pose[0])
        self.pose.setY(pose[1])
        pt = pose[:2] + np.array([np.cos(pose[2]), np.sin(pose[2])]) * self.R
        self.pt.setX(pt[0])
        self.pt.setY(pt[1])
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(QtGui.QPen(Qt.black, 0.5, Qt.SolidLine))
        p.setBrush(QtGui.QBrush(Qt.yellow, Qt.SolidPattern))
        p.drawEllipse(self.pose, self.R, self.R)
        p.drawLine(self.pose, self.pt)
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())