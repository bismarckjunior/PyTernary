# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Mon Mar 17 22:40:11 2014
@email:  bismarckjunior@outlook.com
@brief:  Class that contains the data of Ternary Graph:
            - TernaryPlot
            - headerTableLabels
            - groups: list of lines
"""
from TernaryPlot import TernaryPlot
import numpy as np


class TernaryData():
    def __init__(self, headerLabels, ternaryPlot, canvas):
        self.ternaryPlot = ternaryPlot
        self.canvas = canvas
        self.headerTableLabels = headerLabels
        self.groups = []

    def draw(self):
        self.canvas.draw()

    def add_group(self):
        index = self.ternaryPlot.add_null_plot()
        self.groups.append(index)
        return index

    def add_data(self, index, data):
        self.ternaryPlot.add_data(index, data)
        self.draw()

    def remove_group(self, index):
        if index in self.groups:
            self.groups.remove(index)
            self.ternaryPlot.remove_plot(index)
        self.draw()

    def remove_data(self, index, data):
        self.ternaryPlot.remove_data(index, data)
        self.draw()

    def update_properties(self, index, **kw):
        self.ternaryPlot.change_properties(index, **kw)
        self.draw()

    def update_plot(self, index, data, **kw):
        self.ternaryPlot.update_plot(index, data, **kw)
        self.draw()

    def set_plot_visibility(self, index, toggle):
        self.ternaryPlot.set_plot_visibility(index, toggle)
        self.draw()

    def set_legend_visibility(self, index, toggle):
        self.ternaryPlot.set_legend_visibility(index, toggle)
        self.draw()
        
    def get_plot_visibility(self, index):
        return self.ternaryPlot.get_plot_visibility(index)
    
    def get_legend_visibility(self, index):
        return self.ternaryPlot.get_legend_visibility(index)

    def get_plot_properties(self, index):
        if index in self.groups:
            return self.ternaryPlot.get_properties(index)
        return False


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    fig = plt.figure()
    T = TernaryPlot(fig, short_labels=['SAT', 'NSO', 'ARO'])
    data = [ [10,20,70], [20,25,55], [0.5,0.2,0.3]]
    data = [ [10,20,70], [20,25,55], [0.5,0.2,0.3]]
    group1 = T.plot_data(data, color='green', label='Texto1')
    group2 = T.plot_data([[60,10,30],[25,5,70]])
    t1 = T.plot_template(data+[[40,50,10]],'fill', hatch='/', fill=True, edgecolor='r', color='c')
    #T.legend()
    #T.legend()
    #T.set_plot_visibility(group1, False)
    #T.set_plot_visibility(group2, True)
    #T.clear_plot(t1)
    group3 = T.plot_data([[60,20,30],[25,50,70]])
    T.add_data(group3, [[5,5,90],[10,10,80]])
    #T.set_legend_visibility(t1, True)
    
    #T.inverse()
    T.change_properties(1, markersize=10)
    T.update_plot()
    group4 = T.add_null_plot()
    T.legend()
    
    #T.set_legend_visibility(group4, True)
    T.add_data(group4, [30,30,40])
    T.add_data(group4, [30,30,40])
    T.add_data(group4, [30,30,40])
    T.add_data(group4, [30,30,40])
    T.show()
    
#    import matplotlib.pyplot as plt
#    plt.figure()
#    p = plt.plot(range(4))
#    print p[0].get_data()
#    x= p[0].get_xdata()
#    y= p[0].get_ydata()

#    def remove_dot(x_,y_):
#        x= p[0].get_xdata()
#        y= p[0].get_ydata()
#        xy = zip(x,y)
#        if (x_,y_) in xy:
#            i = xy.index((x_,y_))
#            p[0].set_xdata(np.delete(x, i))
#            p[0].set_ydata(np.delete(y, i))
#    
#    print p[0].get_data()
#    remove_dot(1,1.)
#    #p[0].update(p[0].get_properties())
#    #print dir(p[0])
#    print p[0].get_data()
#    plt.show()