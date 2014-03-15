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
        '''Creates main frame.'''
        self.main_frame = QtGui.QWidget()

        #Creating short title A, B, C
        self.shortTitles = []
        for t in ['A', 'B', 'C']:
            self.shortTitles.append(t)

        #Creating Plot panel
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.TernaryPlot = TernaryPlot(self.fig, short_labels=self.shortTitles)

        #Creating Toolbox for groups
        self.tab = QtGui.QToolBox()
        self.tab.setMaximumWidth(300)
        self.groups = []
        self.groups_brief = []
        self.maxGroupNumber = 0
        self.addGroupTab()

        #Creating buttons for groups
        bbox = QtGui.QHBoxLayout()
        self.btn_addGroup = QtGui.QPushButton('+')
        self.btn_removeGroup = QtGui.QPushButton('-')
        self.btn_editGroups = QtGui.QPushButton('*')

        #Setting buttons shape and tooltip
        self.btn_addGroup.setMaximumWidth(30)
        self.btn_removeGroup.setMaximumWidth(30)
        self.btn_editGroups.setMaximumWidth(30)
        self.btn_addGroup.setToolTip('Add a group')
        self.btn_removeGroup.setToolTip('Remove the current group')
        self.btn_editGroups.setToolTip('Edit the panel labels')

        #Creating layout for buttons
        bbox.addWidget(self.btn_addGroup)
        bbox.addWidget(self.btn_removeGroup)
        bbox.addStretch(1)
        bbox.addWidget(self.btn_editGroups)
        bbox.setSpacing(2)

        #Conecting buttons
        self.connect(self.btn_addGroup, QtCore.SIGNAL('clicked()'),
                     self.addGroupTab)
        self.connect(self.btn_removeGroup, QtCore.SIGNAL('clicked()'),
                     self.removeCurrentGroupTab)
        self.connect(self.btn_editGroups, QtCore.SIGNAL('clicked()'),
                     lambda: PlotSettingsWindow(self, self.TernaryPlot,
                                                self.canvas).exec_())

        #Creating Dock Panel
        pbox = QtGui.QVBoxLayout()
        pbox.addLayout(bbox)
        pbox.addWidget(self.tab)
        pbox.setSpacing(10)
        dock_w = QtGui.QWidget()
        dock_w.setLayout(pbox)
        dock_w.setMaximumWidth(270)
        dock_w.setMinimumWidth(270)
        self.dock = QtGui.QDockWidget(self)
        self.dock.setWidget(dock_w)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock)

        #Creating main_frame
        mbox = QtGui.QHBoxLayout()
        mbox.addWidget(self.canvas)
        self.main_frame.setLayout(mbox)
        self.setCentralWidget(self.main_frame)

    def removeCurrentGroupTab(self):
        '''Remove current tab.'''
        self.removeGroupTab(self.tab.currentIndex())

    def removeGroupTab(self, index):
        '''Removes group tab.'''
        if index == len(self.groups)-1:
            self.maxGroupNumber -= 1
        self.tab.removeItem(index)
        self.tab.setCurrentIndex(index-1)
        self.TernaryPlot.remove_plot(index)

    def addGroupTab(self):
        '''Adds group tab.'''
        table = QtGui.QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(3)
        table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(self.shortTitles)
        table.horizontalHeader().sectionDoubleClicked.connect(self.__changeHorizontalHeader)
        self.__updateRows(table)

        for i in range(3):
            table.setColumnWidth(i, 60)
            table.setItem(0, i, QtGui.QTableWidgetItem(''))

        #Table connections
        table.cellChanged.connect(lambda row, col:
            self.__cellTableChanged(table, row, col, len(self.groups)-1))
        #table.cellActivated.connect(lambda row, col: self.__activatedCellTable(table, row, col))

        #Creating Buttons
        btn_addRow = QtGui.QPushButton('+')
        btn_removeRow = QtGui.QPushButton('-')
        btn_import = QtGui.QPushButton('Im')
        btn_export = QtGui.QPushButton('Ex')

        #Setting buttons shape and tooltips
        btn_addRow.setMaximumWidth(30)
        btn_removeRow.setMaximumWidth(30)
        btn_import.setMaximumWidth(50)
        btn_export.setMaximumWidth(50)
        btn_addRow.setToolTip('Add next row')
        btn_removeRow.setToolTip('Remove current row')
        btn_import.setToolTip('Import data to group')
        btn_export.setToolTip('Export group data')

        #Conecting buttons
        self.connect(btn_addRow, QtCore.SIGNAL('clicked()'),
                     lambda: self.__addRow(table))
        self.connect(btn_removeRow, QtCore.SIGNAL('clicked()'),
                     lambda: self.__removeRow(table))
        self.connect(btn_import, QtCore.SIGNAL('clicked()'),
                     lambda: self.__importData2Table(table, len(self.groups)))
        self.connect(btn_export, QtCore.SIGNAL('clicked()'),
                     lambda: self.__exportData2File(table))

        #Creating button layout
        bbox = QtGui.QHBoxLayout()
        bbox.addWidget(btn_addRow)
        bbox.addWidget(btn_removeRow)
        bbox.addWidget(btn_import)
        bbox.addWidget(btn_export)
        bbox.addStretch()

        #Creating main layout for group
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(table)
        vbox.addLayout(bbox)

        #Updating max group number
        if len(self.groups) == 0:
            self.maxGroupNumber = 0
        self.maxGroupNumber += 1

        #Creating group
        frame = QtGui.QFrame()
        frame.setLayout(vbox)
        groupName = 'Group %d' % self.maxGroupNumber
        self.tab.addItem(frame, groupName)
        self.tab.setCurrentIndex(len(self.groups))

        #Saving group
        self.groups.append([table, btn_import, btn_export])
        self.groups_brief.append('')
        self.TernaryPlot.add_null_plot(label=groupName)

    def __addRow(self, table):
        '''Adds row.'''
        row = table.rowCount() if table.currentRow()==-1 else table.currentRow()+1
        table.insertRow(row)
        self.__updateRows(table)
        
        #Setting selection
        table.setCurrentCell(row, 0)
        for r,s in[(row-1, False), (row, True)]: 
            for col in range(table.columnCount()):
                item = table.item(r, col)
                if not item: table.setItem(r, col, QtGui.QTableWidgetItem(''))
                table.item(r,col).setSelected(s)
    
    def __removeRow(self, table):
        '''Removes row.'''
        if table.rowCount()==1:
            self.__clearRow(table, 0)
            return
        row = table.rowCount()-1 if table.currentRow()==-1 else table.currentRow()
        item = table.item(row, table.currentRow())
        table.removeRow(row)
        self.__updateRows(table)
        
        #Setting selection
        if row==table.rowCount(): row -= 1
        table.setCurrentCell(row, 0)
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if not item: table.setItem(row, col, QtGui.QTableWidgetItem(''))
            table.item(row,col).setSelected(True)
        
    def __clearRow(self, table, row):
        '''Clears row.'''
        for col in range(3):
            table.setItem(row, col, QtGui.QTableWidgetItem(''))
    
    def __updateRows(self, table):
        '''Updates rows.'''
        table.setVerticalHeaderLabels(['%02i' % (i+1) for i in range(table.rowCount())])
        for i in range(table.rowCount()):
            table.setRowHeight(i, 20)
    
    def __changeHorizontalHeader(self, index):
        '''Changes horizontal header.'''
        table = self.groups[0][0]
        oldHeader = table.horizontalHeaderItem(index).text()
        newHeader, ok = QtGui.QInputDialog.getText(self, 
                                                   'Change Header Label', 'Header:', 
                                                   QtGui.QLineEdit.Normal, oldHeader)
        if ok:
            self.shortTitles[index] = newHeader
            self.TernaryPlot.set_short_labels(self.shortTitles)
            self.canvas.draw()
            for table in [t[0] for t in self.groups]:
                table.horizontalHeaderItem(index).setText(newHeader)
                
    def __cellTableChanged(self, table, row, col, index):
        '''Connection to cell table change.'''
        text = table.item(row, col).text()
        
        try:        
            if str(float(text)) != text:
                raise ValueError
        except:
            try:
                text = str(float(text.replace(',','.')))
            except:
                text = ''
            table.item(row, col).setText(text)
            return
                
        line = []
        for i in range(3):
            item = table.item(row, i)
            if item and item.text():
                line.append(float(item.text()) if item.text() else None)
            else:
                line.append(None)

        if line.count(None) == 1:
            i = line.index(None)
            line.remove(None)
            sum_ = sum(line)
            if sum_ <= 1:
                value = 1-sum_
            elif sum_ <= 100:
                value = 100-sum_
            if sum_ <= 100:
                item_ = QtGui.QTableWidgetItem(str(value))
                item_.setBackgroundColor(QtGui.QColor('white'))
                table.setItem(row, i, item_)
        elif None not in line:
            self.__updateGroupPlot(index)

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
                
    def __importData2Table(self, table, index):
        '''Imports data to table.'''
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','./Teste', '*'+self.FORMATFILE)
        if not fname: return
        if not [True for j in range(3) if table.item(table.rowCount()-1,j)]:
            table.removeRow(table.rowCount()-1)
        lines_error = []
        for nline, line in enumerate(open(str(fname.toUtf8()),'r').readlines()):
            line = line.strip()
            if line and line[0] != '#': 
                row = line.split('\t')
                if len(row)<3:
                    row = line.split()
                if len(row)>2:
                    nrow = table.rowCount()
                    table.insertRow(nrow)
                    for col in range(3):
                        cell = row[col] if row[col] != '_' else ''
                        table.setItem(nrow, col, QtGui.QTableWidgetItem(cell))
                        self.__cellTableChanged(table, nrow, col, index)
                else:
                    lines_error.append(str(nline+1))
                    
        self.__updateRows(table)
        
        #Warning Message
        if lines_error:
            wm = QtGui.QMessageBox(self)
            wm.setWindowTitle('Warning')
            msg = '<h2 align="center">Warning</h2> <p>Problems in line(s): %s</p>'
            if len(lines_error)>5:
                lines_error = lines_error[:5]+['...']
            wm.setText(msg % ', '.join(lines_error))
            wm.show()
                        
    def __exportData2File(self, table):
        '''Exports datat to file.'''
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file','./Teste', '*'+ self.FORMATFILE)
        if not fname: return
        if not fname.endsWith(self.FORMATFILE):
            fname += self.FORMATFILE 
        f = open(str(fname.toUtf8()), 'w')
        f.write('#%s\t%s\t%s\n' % tuple([t.text() for t in self.shortTitles]))
        for row in range(table.rowCount()):
            for col in range(3):
                item = table.item(row, col) 
                f.write('%s\t' % (item.text() if item and item.text() else '_'))
            f.write('\n')
        f.close()
    
    
###############################################################################
class QGroupTable(QtGui.QTableWidget):
    def __init__(self, parent, shortTitle):
        super(QGroupTable, self).__init__(None)
        self.setRowCount(1)
        self.setColumnCount(3)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(self.shortTitles)
        table.horizontalHeader().sectionDoubleClicked.connect(self.__changeHorizontalHeader)
        self.__updateRows(table)

        for i in range(3):
            self.setColumnWidth(i, 60)
            self.setItem(0, i, QtGui.QTableWidgetItem(''))

        #Table connections
        self.cellChanged.connect(lambda row, col:
        self.__cellTableChanged(table, row, col, len(self.groups)-1))
        #table.cellActivated.connect(lambda row, col: self.__activatedCellTable(table, row, col))

        #Creating Buttons
        btn_addRow = QtGui.QPushButton('+')
        btn_removeRow = QtGui.QPushButton('-')
        btn_import = QtGui.QPushButton('Im')
        btn_export = QtGui.QPushButton('Ex')

        #Setting buttons shape and tooltips
        btn_addRow.setMaximumWidth(30)
        btn_removeRow.setMaximumWidth(30)
        btn_import.setMaximumWidth(50)
        btn_export.setMaximumWidth(50)
        btn_addRow.setToolTip('Add next row')
        btn_removeRow.setToolTip('Remove current row')
        btn_import.setToolTip('Import data to group')
        btn_export.setToolTip('Export group data')

        #Conecting buttons
        self.connect(btn_addRow, QtCore.SIGNAL('clicked()'),
                     lambda: self.__addRow(table))
        self.connect(btn_removeRow, QtCore.SIGNAL('clicked()'),
                     lambda: self.__removeRow(table))
        self.connect(btn_import, QtCore.SIGNAL('clicked()'),
                     lambda: self.__importData2Table(table, len(self.groups)))
        self.connect(btn_export, QtCore.SIGNAL('clicked()'),
                     lambda: self.__exportData2File(table))

        #Creating button layout
        bbox = QtGui.QHBoxLayout()
        bbox.addWidget(btn_addRow)
        bbox.addWidget(btn_removeRow)
        bbox.addWidget(btn_import)
        bbox.addWidget(btn_export)
        bbox.addStretch()

        #Creating main layout for group
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(table)
        vbox.addLayout(bbox)

        #Updating max group number
        if len(self.groups) == 0:
            self.maxGroupNumber = 0
        self.maxGroupNumber += 1

        #Creating group
        frame = QtGui.QFrame()
        frame.setLayout(vbox)
        groupName = 'Group %d' % self.maxGroupNumber
        self.tab.addItem(frame, groupName)
        self.tab.setCurrentIndex(len(self.groups))

        #Saving group
        self.groups.append([table, btn_import, btn_export])
        self.groups_brief.append('')
        self.TernaryPlot.add_null_plot(label=groupName)

        
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
    
    
    
    
    
    
    
    
    
