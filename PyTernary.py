# -*- coding: utf-8 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sat Mar 15 09:30:52 2014
@email:  bismarckjunior@outlook.com
@brief:  PyTernary is a GUI to plot a Ternary graph. 
"""
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
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
        self.setWindowTitle('TernaryPlot')

        self.plots = {'view': {'groups': []}}

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

###############################################################################
  
class PlotSettingsWindow(QtGui.QDialog):
    def __init__(self, parent, TernaryPlot, canvas):
        '''Constructor. 
        plots: plot data
        canvas: canvas to plot
        '''
        super(PlotSettingsWindow, self).__init__(None)
        self.setWindowTitle('Plot Settings')
        self.TernaryPlot = TernaryPlot
        self.canvas = canvas
        self.parent = parent
        self.markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4',
                        's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_']
        self.create_main_frame()
        
    def create_main_frame(self):
        #Tab Box
        tabBox = QtGui.QTabWidget()

        #Tab Box: Elements
        self.elements_table = QtGui.QTableWidget()
        self.elements_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.elements_table.verticalHeader().setVisible(False)
        self.elements_table.setColumnCount(6)
        self.elements_table.setHorizontalHeaderLabels(['Name', 'Color', 'Marker', 'Size', 'Plot', 'Legend'])
        self.__addElementsTable()
        columnsWidth = [150] + [60]*5
        for i, column in enumerate(columnsWidth):
            self.elements_table.setColumnWidth(i, column)
        tabBox.addTab(self.elements_table, 'Elements')

        #Tab Box: Title

        #Creating main_frame
        mbox = QtGui.QVBoxLayout()
        mbox.addWidget(tabBox)
        self.setLayout(mbox)
        self.setGeometry(QtCore.QRect(10, 50, 500, 350))

    def __connect(self, dic, key, value):
        '''Connects the value to a dictionary.'''
        dic[key] = value
        self.canvas.draw()
    
    def __addElementsTable(self):
        '''Adds elements table.'''
        self.frmColor = []
        self.chkBoxPlot = []
        self.chkBoxLegend = []
        for row in range(self.TernaryPlot.get_n()):
            self.__addRow2ElementsTable(row)
        #Connections
        self.elements_table.cellClicked.connect(self.__setCellColor)
        self.elements_table.cellChanged.connect(self.__setNewGroupName)
        self.elements_table.horizontalHeader().sectionClicked.connect(self.__changeCheckBoxesColumn)

    def __setNewGroupName(self, row, col):
        if col == 0:
            newGroupName = self.elements_table.item(row, col).text()
            if newGroupName:
                self.TernaryPlot.change_properties(row, label = newGroupName)
                self.parent.tab.setItemText(row, newGroupName)

    def __changeCheckBoxesColumn(self, index):
        if index == 4:
            for i in range(self.TernaryPlot.get_n()):
                chkValue = not self.TernaryPlot.get_plot_visibility(i)
                self.TernaryPlot.set_plot_visibility(i, chkValue)
                self.chkBoxPlot[i].setCheckState(QtCore.Qt.Checked if chkValue else QtCore.Qt.Unchecked)
        if index == 5:
            for i in range(self.TernaryPlot.get_n()):
                chkValue = not self.TernaryPlot.get_legend_visibiliy(i)
                self.TernaryPlot.set_legend_visibility(i, chkValue)
                self.chkBoxLegend[i].setCheckState(QtCore.Qt.Checked if chkValue else QtCore.Qt.Unchecked)
        
    def __setCellColor(self, row, col):
        if col==1:
            color = QtGui.QColorDialog.getColor()
            if color.isValid():
                self.TernaryPlot.change_properties(row, color=color.name())
                self.frmColor[row].setStyleSheet("QWidget {background-color: %s}" % color.name())
       
    def __addRow2ElementsTable(self, row):
        '''Adds row to elements table.'''
        table = self.elements_table
        table.insertRow(row)
        table.setRowHeight(row, 22)

        #Label
        item = QtGui.QTableWidgetItem(self.TernaryPlot.get_properties(row, 'label'))
        table.setItem(row, 0, item)

        #Color
        color = QtGui.QColor(self.TernaryPlot.get_properties(row, 'color'))
        self.frmColor.append(QtGui.QFrame())
        self.frmColor[-1].setStyleSheet("QWidget {background-color: %s}" % color.name())
        table.setCellWidget(row, 1, self.frmColor[-1])
#        table.cellClicked.connect(lambda x,y: self.setCellColor(x, y, frm))
        
        #Marker
        comboBox = QtGui.QComboBox()
        comboBox.addItems(self.markers)
        marker = self.TernaryPlot.get_properties(row)
        comboBox.setCurrentIndex(self.markers.index(marker['marker']))
        comboBox.currentIndexChanged.connect(lambda x:self.__connect(marker,'marker', self.markers[x]))
        table.setCellWidget(row, 2, comboBox)

        #Marker size
        sbox = QtGui.QSpinBox()
        d_markersize = self.TernaryPlot.get_properties(row)
        sbox.setValue(d_markersize['markersize'])
        sbox.setMinimum(1)
        sbox.setMaximum(30)
        sbox.valueChanged.connect(lambda x:self.__connect(d_markersize, 'markersize', x))
        table.setCellWidget(row, 3, sbox)
                
        #Plot
        chkValue = self.TernaryPlot.get_plot_visibility(row)
        frame = QtGui.QFrame()
        chkBoxPlot = QtGui.QCheckBox('')
        chkBoxPlot.setCheckState(QtCore.Qt.Checked if chkValue else QtCore.Qt.Unchecked)
        chkBoxPlot.clicked.connect(lambda x: self.TernaryPlot.set_plot_visibility(row, x))
        self.chkBoxPlot.append(chkBoxPlot)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(chkBoxPlot)
        hbox.addStretch(1)
        hbox.setMargin(2)
        frame.setLayout(hbox)
        table.setCellWidget(row, 4, frame)
        
        #Legend
        frame = QtGui.QFrame()
        chkValue = self.TernaryPlot.get_legend_visibility(row)
        chkBoxLegend = QtGui.QCheckBox('')
        chkBoxLegend.setCheckState(QtCore.Qt.Checked if chkValue else QtCore.Qt.Unchecked)
        chkBoxLegend.clicked.connect(lambda x: self.TernaryPlot.set_legend_visibility(row, x))
        self.chkBoxLegend.append(chkBoxLegend)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(chkBoxLegend)
        hbox.addStretch(1)
        hbox.setMargin(2)
        frame.setLayout(hbox)
        table.setCellWidget(row, 5, frame)            
          
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    main = PyTernary()
    main.show()
    sys.exit(app.exec_())
    
    
    
    
    
    
    
    
    
