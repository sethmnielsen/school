import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import msdParam as P


class msdAnimation:
    '''
        Create msd animation
    '''
    def __init__(self):
        self.flagInit = True                  # Used to indicate initialization
        self.fig, self.ax = plt.subplots()    # Initializes a figure and axes object
        self.handle = []                      # Initializes a list object that will
                                              # be used to contain handles to the
                                              # patches and line objects.
        a = 4.0
        self.length=P.w*a
        self.width=P.h*a
        plt.axis([-a*P.w, a*P.w, -a*P.w, a*P.w]) # Change the x,y axis limits
        plt.grid(True)
        plt.plot([0, P.w], [0, 0],'k--')         # Draw a base line

        # Draw pendulum is the main function that will call the functions:
        # drawCart, drawCircle, and drawRod to create the animation.
    def drawmsd(self, u):
        # Process inputs to function
        z = u[0]   # angle of msd, rads

        self.drawMass(z)
        self.drawSpring(z)
        self.drawDamper(z)
        self.ax.axis('equal') # This will cause the image to not distort

        # After each function has been called, initialization is over.
        if self.flagInit == True:
            self.flagInit = False

    def drawMass(self, z):
        x = z-P.w/2.0  # x coordinate
        y = 0          # y coordinate
        xy = (x, y)     # Bottom left corner of rectangle

        # When the class is initialized, a Rectangle patch object will be
        # created and added to the axes. After initialization, the Rectangle
        # patch object will only be updated.
        if self.flagInit == True:
            # Create the Rectangle patch and append its handle
            # to the handle list
            self.handle.append(mpatches.Rectangle(xy,P.w,P.h, fc = 'blue', ec = 'black'))
            self.ax.add_patch(self.handle[0]) # Add the patch to the axes
        else:
            self.handle[0].set_xy(xy)         # Update patch


    def drawSpring(self, z):
        x1 = np.array([-10.0, -9.0, z-4.0, z-4.0, z-2.0])
        y1 = [0, 0, 0, .5, -.5, .5, -.5, .5, -.5, .5, -.5, 0, 0, 0]

        x = np.insert(x1, 2, np.linspace(-9, z-4, num=9, endpoint=False)).tolist()
        y = [i+P.c+1 for i in y1]

        # When the class is initialized, a CirclePolygon patch object will
        # be created and added to the axes. After initialization, the
        # CirclePolygon patch object will only be updated.
        if self.flagInit == True:
            # Create the CirclePolygon patch and append its handle
            # to the handle list
            line, =self.ax.plot(x, y, lw=1, c='green')
            self.handle.append(line)
        else:
            self.handle[1].set_xdata(x)
            self.handle[1].set_ydata(y)


    def drawDamper(self, z):
        # Damper
        X1 = [-10, -9]
        X2 = [-9, -9]
        X3 = [z-10.0, z-4.0, z-4.0, z-10.0]
        X4 = [z-4.0, z-2.0]
        a = P.c-0.8
        Y1 = [a, a]
        Y2 = [0.5+a, -0.5+a]
        Y3 = [0.6+a, 0.6+a, -0.6+a, -0.6+a]
        Y4 = [a, a]

        # When the class is initialized, a line object will be
        # created and added to the axes. After initialization, the
        # line object will only be updated.
        if self.flagInit == True:
            # Create the line object and append its handle
            # to the handle list.
            line1, =self.ax.plot(X1,Y1,lw = 1, c = 'black')
            line2, =self.ax.plot(X2,Y2,lw = 1, c = 'black')
            line3, =self.ax.plot(X3,Y3,lw = 1, c = 'black')
            line4, =self.ax.plot(X4,Y4,lw = 1, c = 'black')
            self.handle.append(line1)
            self.handle.append(line2)
            self.handle.append(line3)
            self.handle.append(line4)
        else:
            self.handle[2].set_xdata(X1)               # Update the line
            self.handle[2].set_xdata(X2)               # Update the line
            self.handle[2].set_xdata(X3)               # Update the line
            self.handle[2].set_xdata(X4)               # Update the line
            self.handle[2].set_ydata(Y1)
            self.handle[2].set_ydata(Y2)
            self.handle[2].set_ydata(Y3)
            self.handle[2].set_ydata(Y4)


# Used see the animation from the command line
if __name__ == "__main__":

    simAnimation = msdAnimation()           # Create Animate object
    theta = 0.0*np.pi/180                   # Angle of msd, rads
    simAnimation.drawmsd([z, theta, 0, 0])  # Draw the msd
    #plt.show()
    # Keeps the program from closing until the user presses a button.
    print('Press key to close')
    plt.waitforbuttonpress()
    plt.close()
