import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import vtolParam as P
import seaborn as sns
sns.set_style("white")

class vtolAnimation:
    '''
        Create vtol animation
    '''
    def __init__(self):
        self.flagInit = True                  # Used to indicate initialization
        self.fig, self.ax = plt.subplots()    # Initializes a figure and axes object
        self.handle = []                      # Initializes a list object that will
                                              # be used to contain handles to the
                                              # patches and line objects.
        plt.axis([0, 7, 0, 7]) # Change the x,y axis limits
        plt.grid(True)
        plt.xlabel('z')

        # Draw pendulum is the main function that will call the functions:
        # drawCart, drawCircle, and drawRod to create the animation.
    def drawvtol(self, u):
        # Process inputs to function
        z = u[0]
        h = u[1]
        th = u[2]

        self.drawBody (z, h, th)
        self.drawProps(z, h, th)
        # self.ax.axis('equal') # This will cause the image to not distort

        # After each function has been called, initialization is over.
        if self.flagInit == True:
            self.flagInit = False

    def drawBody(self, z, h, th):
        a = P.w/2.0
        pts = np.matrix([
                [-a, -a],
                [ a, -a],
                [ a,  a],
                [-a,  a]])

        R = np.matrix([[np.cos(th), np.sin(th)],
                       [-np.sin(th), np.cos(th)]])
        T = np.matrix([z,h])
        xy = np.array((pts*R) + T)

        # When the class is initialized, a Rectangle patch object will be
        # created and added to the axes. After initialization, the Rectangle
        # patch object will only be updated.
        if self.flagInit == True:
            # Create the Rectangle patch and append its handle
            # to the handle list
            rect = mpatches.Polygon(xy, fc = 'blue', ec = 'black')
            self.handle.append(rect)
            self.ax.add_patch(self.handle[0]) # Add the patch to the axes
        else:
            self.handle[0].set_xy(xy)         # Update patch

    def drawProps(self, z, h, th):
        R = np.matrix([[np.cos(th), np.sin(th)], [-np.sin(th), np.cos(th)]])
        xr = z + P.d*np.cos(th)
        yr = h + P.d*np.sin(th)
        # pr = np.matrix([xr,y]) * R
        # xyr = (pr.item(0), pr.item(1))
        xyr = (xr, yr)

        xl = z - P.d*np.cos(th)
        yl = h - P.d*np.sin(th)
        # pl = np.matrix([xl,y]) * R
        # xyl = (pl.item(0), pl.item(1))
        xyl = (xl, yl)

        # When the class is initialized, a CirclePolygon patch object will
        # be created and added to the axes. After initialization, the
        # CirclePolygon patch object will only be updated.
        if self.flagInit == True:
            # Create the CirclePolygon patch and append its handle
            # to the handle list
            self.handle.append(mpatches.CirclePolygon(xyr,
                radius = P.r, resolution = 15,
                fc = 'limegreen', ec = 'black'))
            self.handle.append(mpatches.CirclePolygon(xyl,
                radius = P.r, resolution = 15,
                fc = 'limegreen', ec = 'black'))
            self.ax.add_patch(self.handle[1])  # Add the patch to the axes
            self.ax.add_patch(self.handle[2])  # Add the patch to the axes
        else:
            self.handle[1]._xy=xyr
            self.handle[2]._xy=xyl


# Used see the animation from the command line
if __name__ == "__main__":

    # simAnimation = vtolAnimation()        # Create Animate object
    # th = 0.0*np.pi/180                    # Angle of vtol, rads
    # simAnimation.drawvtol([z, th, 0, 0])  # Draw the vtol
    #plt.show()
    # Keeps the program from closing until the user presses a button.
    print('Press key to close')
    plt.waitforbuttonpress()
    plt.close()
