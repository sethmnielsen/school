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

Once you have completed this, you can play around creating other maps if you like using these m-files.


######## file that mat gave me ########

import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

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

        #  image plot
        self.img = pg.ImageItem(border='w')
        self.view.addItem(self.img)

        self.canvas.nextRow()
        #  line plot
        self.otherplot = self.canvas.addPlot()
        self.h2 = self.otherplot.plot(pen='y')


        #### Set Data  #####################

        self.x = np.linspace(0,50., num=100)
        self.X,self.Y = np.meshgrid(self.x,self.x)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################
        self._update()

    def _update(self):

        self.data = np.sin(self.X/3.+self.counter/9.)*np.cos(self.Y/3.+self.counter/9.)
        self.ydata = np.sin(self.x/3.+ self.counter/9.)

        self.img.setImage(self.data)
        self.h2.setData(self.ydata)

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
        self.counter += 1


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())

'''

