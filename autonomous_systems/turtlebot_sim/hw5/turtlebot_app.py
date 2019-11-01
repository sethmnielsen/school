import sys
import time
import numpy as np

from PyQt5.QtCore import Qt
from pyqtgraph.Qt import QtCore, QtGui
# from pyqtgraph import QtCore, QtGui, Qt
import pyqtgraph as pg

from hw5.og_mapping import OGMapping
import hw5.params as pm

class App(QtGui.QMainWindow):
    def __init__(self, x_state, z, thk, parent=None):
        super(App, self).__init__(parent)

        self.x_state = x_state
        self.z_r, self.z_phi = z
        self.ogmap = OGMapping(thk)
        self.probs = np.ones((pm.n, pm.n)) * 0.5
        self.data = np.zeros((pm.n, pm.n))
        
        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.setRange(QtCore.QRectF(0,0, 100, 100))

        #### Set Data  #####################
        self.x = np.linspace(0,200., num=100)
        self.X,self.Y = np.meshgrid(self.x,self.x)

        #  image plot
        self.img = pg.ImageItem(border='w')
        self.view.addItem(self.img)
        self.turtlebot = TurtleApp(self.X[:,10], 1.5) 
        self.view.addItem(self.img)
        self.view.addItem(self.turtlebot)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()

    def _update(self):
        if self.counter < self.x_state.shape[1]:
            Xt = self.x_state[:,self.counter]
            z_rt = self.z_r[:,self.counter]
            z_phit = self.z_phi[:,self.counter]

            self.probs = self.ogmap.update_map( Xt, z_rt, z_phit )

            self.turtlebot.setPose(self.x_state[:,self.counter])
            self.counter += 1
            # time.sleep(0.05)
            self.counter += 1
        else:
            print(self.probs.T)
            sys.exit()

        self.data = 255 - self.probs * 255
        self.img.setImage(self.data) 

        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)
        QtCore.QTimer.singleShot(1, self._update)

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
