import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.ion()  # enable interactive drawing


class plotData:
    '''
        This class plots the time histories for the pendulum data.
    '''

    def __init__(self):
        # Number of subplots = num_of_rows*num_of_cols
        self.num_rows = 2    # Number of subplot rows
        self.num_cols = 1    # Number of subplot columns

        # Crete figure and axes handles
        self.fig, self.ax = plt.subplots(self.num_rows, self.num_cols, sharex=True)

        # Instantiate lists to hold the time and data histories
        self.time_history = []  # time
        self.z_ref_history = []  # reference angle
        self.h_ref_history = []  # reference angle
        self.th_ref_history = []  # reference angle
        self.z_history = []  # angle z
        self.h_history = []  # angle z
        self.th_history = []  # angle z
        self.fl_history = []  # control force
        self.fr_history = []  # control force
        self.force_history = []  # control force

        # create a handle for every subplot.
        self.handle = []
        self.handle.append(myPlot(self.ax[0], ylabel='z', title='VTOL Data'))
        # self.handle.append(myPlot(self.ax[0], ylabel='Angle (deg)', title='VTOL Data'))
        # self.handle.append(myPlot(self.ax[1], ylabel='fl (N)'))
        self.handle.append(myPlot(self.ax[1], xlabel='t(s)', ylabel='h'))

    def updatePlots(self, t, reference, states, ctrl):
        '''
            Add to the time and data histories, and update the plots.
        '''
        # update the time history of all plot variables
        self.time_history.append(t)  # time
        self.z_history.append(states[0])  # rod angle (converted to degrees)
        self.z_ref_history.append(reference[0])  # reference base position
        self.h_history.append(states[1])  # rod angle (converted to degrees)
        self.h_ref_history.append(reference[1])  # reference base position
        # self.th_history.append(states[2]*180/np.pi)  # rod angle (converted to degrees)
        # self.force_history.append(ctrl[1])  # force on the base
        # self.fl_history.append(reference[0])  # force on the base
        # self.fr_history.append(reference[1])  # force on the base

        # update the plots with associated histories
        self.handle[0].updatePlot(self.time_history, [self.z_history, self.z_ref_history])
        # self.handle[0].updatePlot(self.time_history, [self.th_history])
        self.handle[1].updatePlot(self.time_history, [self.h_history, self.h_ref_history])
        # self.handle[1].updatePlot(self.time_history, [self.force_history])
        # self.handle[0].updatePlot(self.time_history, [self.fl_history])
        # self.handle[1].updatePlot(self.time_history, [self.fr_history])


class myPlot:
    '''
        Create each individual subplot.
    '''
    def __init__(self, ax,
                 xlabel='',
                 ylabel='',
                 title='',
                 legend=None):
        '''
            ax - This is a handle to the  axes of the figure
            xlable - Label of the x-axis
            ylable - Label of the y-axis
            title - Plot title
            legend - A tuple of strings that identify the data.
                     EX: ("data1","data2", ... , "dataN")
        '''
        self.legend = legend
        self.ax = ax                  # Axes handle
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'b']
        # A list of colors. The first color in the list corresponds
        # to the first line object, etc.
        # 'b' - blue, 'g' - green, 'r' - red, 'c' - cyan, 'm' - magenta
        # 'y' - yellow, 'k' - black
        self.line_styles = ['-', '-', '--', '-.', ':']
        # A list of line styles.  The first line style in the list
        # corresponds to the first line object.
        # '-' solid, '--' dashed, '-.' dash_dot, ':' dotted

        self.line = []

        # Configure the axes
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel)
        self.ax.set_title(title)
        self.ax.grid(True)

        # Keeps track of initialization
        self.init = True

    def updatePlot(self, time, data):
        '''
            Adds data to the plot.
            time is a list,
            data is a list of lists, each list corresponding to a line on the plot
        '''
        if self.init == True:  # Initialize the plot the first time routine is called
            for i in range(len(data)):
                # Instantiate line object and add it to the axes
                self.line.append(Line2D(time,
                                        data[i],
                                        color=self.colors[np.mod(i, len(self.colors) - 1)],
                                        ls=self.line_styles[np.mod(i, len(self.line_styles) - 1)],
                                        label=self.legend if self.legend != None else None))
                self.ax.add_line(self.line[i])
            self.init = False
            # add legend if one is specified
            if self.legend != None:
                plt.legend(handles=self.line)
        else: # Add new data to the plot
            # Updates the x and y data of each line.
            for i in range(len(self.line)):
                self.line[i].set_xdata(time)
                self.line[i].set_ydata(data[i])

        # Adjusts the axis to fit all of the data
        self.ax.relim()
        self.ax.autoscale()
