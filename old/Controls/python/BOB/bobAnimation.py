import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import bobParam as P
import seaborn as sns
sns.set_style("white")

class bobAnimation:
    '''
        Create bob animation
    '''
    def __init__(self):
        self.flagInit = True                  # Used to indicate initialization
        self.fig, self.ax = plt.subplots()    # Initializes a figure and axes object
        self.handle = []                      # Initializes a list object that will
                                              # be used to contain handles to the
                                              # patches and line objects.
        plt.axis([-1*P.ell,2*P.ell, -0.1, 2*P.ell]) # Change the x,y axis limits
        plt.plot([-1*P.ell,1*P.ell],[0,0],'b--')    # Draw a base line
        plt.xlabel('z')

        # Draw pendulum is the main function that will call the functions:
        # drawCart, drawCircle, and drawRod to create the animation.
    def drawbob(self, u):
        # Process inputs to function
        z = u[0]        # Horizontal position of cart, m
        th = u[1]       # Angle of pendulum, rads

        # print z

        self.drawBeam(th)
        self.drawBall(z, th)
        # self.drawRod(z, th)
        self.ax.axis('equal') # This will cause the image to not distort

        # After each function has been called, initialization is over.
        if self.flagInit == True:
            self.flagInit = False

    def drawBeam(self, th):

        X = [0, P.ell*np.cos(th)]  # X data points
        Y = [0, P.ell*np.sin(th)]  # Y data points

        # When the class is initialized, a line object will be
        # created and added to the axes. After initialization, the
        # line object will only be updated.
        if self.flagInit == True:
            # Create the line object and append its handle
            # to the handle list.
            line, =self.ax.plot(X, Y, lw=5, c='blue')
            self.handle.append(line)
            # self.flagInit=False
        else:
            self.handle[0].set_xdata(X)   # Update the line
            self.handle[0].set_ydata(Y)

    def drawBall(self, z, th):
        # x = z+(P.radius)*np.sin(th)         # x coordinate
        # y = P.radius*np.cos(th)             # y coordinate
        # xy = (x,y)                                   # Center of circle

        R = np.matrix([[np.cos(th), np.sin(th)], [-np.sin(th), np.cos(th)]])
        x = z + P.radius
        y = P.radius
        A = np.matrix([x,y]) * R
        xy = (A.item(0), A.item(1))

        # When the class is initialized, a CirclePolygon patch object will
        # be created and added to the axes. After initialization, the
        # CirclePolygon patch object will only be updated.
        if self.flagInit == True:
            # Create the CirclePolygon patch and append its handle
            # to the handle list
            self.handle.append(mpatches.CirclePolygon(xy,
                radius = P.radius, resolution = 15,
                fc = 'limegreen', ec = 'black'))
            self.ax.add_patch(self.handle[1])  # Add the patch to the axes
        else:
            self.handle[1]._xy=xy

    # def drawRod(self, z, th):
    #     X = [z,z+P.ell*np.sin(th)]                  # X data points
    #     Y = [P.gap+P.h, P.gap+P.h+P.ell*np.cos(th)] # Y data points
    #
    #     # When the class is initialized, a line object will be
    #     # created and added to the axes. After initialization, the
    #     # line object will only be updated.
    #     if self.flagInit == True:
    #         # Create the line object and append its handle
    #         # to the handle list.
    #         line, =self.ax.plot(X,Y,lw = 1, c = 'black')
    #         self.handle.append(line)
    #     else:
    #         self.handle[2].set_xdata(X)               # Update the line
    #         self.handle[2].set_ydata(Y)

# Used see the animation from the command line
if __name__ == "__main__":

    simAnimation = bobAnimation()           # Create Animate object
    th = 0.0*np.pi/180                   # Angle of bob, rads
    simAnimation.drawbob([z, th, 0, 0])  # Draw the bob
    #plt.show()
    # Keeps the program from closing until the user presses a button.
    print('Press key to close')
    plt.waitforbuttonpress()
    plt.close()
