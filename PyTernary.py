# -*- coding: utf-8 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sat Mar 15 09:30:52 2014
@email:  bismarckjunior@outlook.com
@brief:  PyTernary is a GUI to plot a Ternary graph. 

#TODO:
    * Mudar posiçao do ternarySettingsFrame
    * Mudar posicao tamanho da fonte
    * grupos da tabela e do plot diferentes
        - Adicione grupo 2 e 3
        - Remova o grupo 2, 1 e 3 
"""
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from TernaryPlot import TernaryPlot 
from TernaryData import TernaryData
from GroupsFrame import GroupsFrame
import sys


class PyTernary(QtGui.QMainWindow):
    FORMATFILE = '.dat'

    def __init__(self, parent=None):
        '''Constructor.'''
        super(PyTernary, self).__init__(parent)
        self.setWindowTitle('PyTernary')

        #Creating main frame
        self.create_main_frame()

    def create_main_frame(self):
        main_frame = QtGui.QWidget()

        short_labels = ['A', 'B', 'C']

        #Creating Plot panel
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(main_frame)

        #Creating TernaryPlot
        ternaryPlot = TernaryPlot(self.fig, short_labels=short_labels)

        #Creating TernaryData
        self.ternaryData = TernaryData(short_labels, ternaryPlot, self.canvas)

        #Creating Dock Panel
        groupsFrame = GroupsFrame(self.ternaryData)
        self.dock = QtGui.QDockWidget(self)
        self.dock.setMaximumWidth(270)
        self.dock.setMinimumWidth(270)
        self.dock.setWidget(groupsFrame)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock)

        #Creating main_frame
        mbox = QtGui.QHBoxLayout()
        mbox.addWidget(self.canvas)
        main_frame.setLayout(mbox)
        self.setCentralWidget(main_frame)

    def __updateGroupPlot(self, index):
        '''Updates the plot for group in "index" position.'''
        data = self.__getGroupData(index)
        if data:
            self.TernaryPlot.update_plot(index, data)
            self.canvas.draw()

    def __getGroupData(self, index):
        '''Gets group data as a matrix (type: list).'''
        data = []
        table = self.groups[index][0]
        for row in range(table.rowCount()):
            try:
                line = [float(table.item(row, col).text()) for col in range(3)]
            except:
                continue
            data.append(line)
        return data    
          
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    main = PyTernary()
    main.show()
    sys.exit(app.exec_())
    
    
    
    
    
    
    
    
    
