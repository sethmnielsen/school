import sys
import time
import numpy as np

from PyQt5.QtCore import Qt
from pyqtgraph.Qt import QtCore, QtGui, Qt
import pyqtgraph as pg

class TurtleBotItem(pg.GraphicsObject):
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