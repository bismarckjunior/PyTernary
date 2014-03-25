# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sun Mar 16 20:08:55 2014
@email:  bismarckjunior@outlook.com
@brief:  Frame for groups: QToolbox whith QTableWidget
"""
from PyQt4 import QtGui, QtCore
from TernaryTableData import TernaryTableData
import sys


class TableFrame(QtGui.QFrame):
    FORMATFILE = '.dat'

    def __init__(self, ternaryData, parent=None):
        super(TableFrame, self).__init__(parent)
        self.table = TernaryTableData(ternaryData)
        self.table.setGeometry(QtCore.QRect(10, 50, 700, 350))

        #Buttons
        btn_import = QtGui.QPushButton('Im')
        btn_export = QtGui.QPushButton('Ex')

        #Setting buttons shape and tooltips
        btn_import.setMaximumWidth(50)
        btn_export.setMaximumWidth(50)
        btn_import.setToolTip('Import data to group')
        btn_export.setToolTip('Export group data')

        #Conecting buttons
        self.connect(btn_import, QtCore.SIGNAL('clicked()'),
                     self.__importData2Table)
        self.connect(btn_export, QtCore.SIGNAL('clicked()'),
                     self.__exportData2File)

        #Creating button layout
        bbox = QtGui.QHBoxLayout()
        bbox.addWidget(btn_import)
        bbox.addWidget(btn_export)
        bbox.addStretch()
        bbox.setSpacing(2)

        #Creating main layout for group
        mainBox = QtGui.QVBoxLayout()
        mainBox.addWidget(self.table)
        mainBox.addLayout(bbox)

        self.setLayout(mainBox)

    def __importData2Table(self):
        '''Imports data to table.'''
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                  './Groups',
                                                  '*' + self.FORMATFILE)
        if not fname:
            return

        data = open(str(fname.toUtf8()), 'r').readlines()

        lines_error = []
        for nline, line in enumerate(data):
            line = line.strip()
            if line and line[0] != '#':
                row = line.split()
                if len(row) > 2:
                    nrow = self.table.rowCount()-1
                    self.table.insertRow(nrow)
                    for col in range(3):
                        cell = row[col] if row[col] != '-' else ''
                        self.table.setItem(nrow, col,
                                           QtGui.QTableWidgetItem(cell))
                else:
                    lines_error.append(str(nline+1))

        self.table.updateRows()
        #TODO: update_plot

        #Warning Message
        if lines_error:
            wm = QtGui.QMessageBox(self)
            wm.setWindowTitle('PyTernary')
            msg = '''<h2 align="center">Warning</h2>
                     <center>Problems in line(s): %s. </center>'''
            if len(lines_error) > 5:
                lines_error = lines_error[:5]+['..']
            wm.setText(msg % ', '.join(lines_error))
            wm.show()

    def __exportData2File(self):
        '''Exports datat to file.'''
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file',
                                                  './Groups',
                                                  '*' + self.FORMATFILE)
        if not fname:
            return

        if not fname.endsWith(self.FORMATFILE):
            fname += self.FORMATFILE  # TODO: testar

        f = open(str(fname.toUtf8()), 'w')
        header = [h.strip() for h in self.headerLabels]
        f.write('#{:9} {:10} {:10}\n'.format(*header))
        for row in range(self.table.rowCount()-1):
            line = []
            for col in range(3):
                item = self.table.item(row, col)
                line.append(str(item.text()) if item and item.text() else '-')
            f.write('{:10} {:10} {:10}\n'.format(*line))
        f.close()


class GroupsToolBox(QtGui.QToolBox):
    def __init__(self, ternaryData, parent=None):
        super(GroupsToolBox, self).__init__(parent)
        self.ternaryData = ternaryData
        self.ternaryData.renameTableHeaders = self.renameTableHeaders
        self.setMaximumWidth(300)
        self.frames = []
        self.addTab()

    def addTab(self):
        #Updating max tab number
        if self.count() == 0:
            self.maxTabNumber = 0
        self.maxTabNumber += 1

        frame = TableFrame(self.ternaryData)
        frame.setMinimumHeight(200)
        self.frames.append(frame)
        TabName = 'Group %d' % self.maxTabNumber
        self.addItem(frame, TabName)
        self.setCurrentIndex(self.count()-1)

    def removeCurrentTab(self):
        self.removeTab(self.currentIndex())

    def renameTableHeaders(self, tableHeaders):
        for frame in self.frames:
            frame.table.setHorizontalHeaderLabels(tableHeaders)

    def removeTab(self, index):
        if self.count() == 1:
            self.removeItem(0)
            frame = self.frames.pop(index)
            self.ternaryData.remove_group(frame.table.index)
            self.addTab()
            return
        if index == self.count()-1:
            self.maxTabNumber -= 1
        self.removeItem(index)
        frame = self.frames.pop(index)
        self.ternaryData.remove_group(frame.table.index)
        self.setCurrentIndex(index-1)
        #TODO: update_plot


class GroupsFrame(QtGui.QFrame):
    def __init__(self, ternaryData, parent=None):
        super(GroupsFrame, self).__init__(parent)

        toolBox = GroupsToolBox(ternaryData)

        #Buttons
        btn_addGroup = QtGui.QPushButton('+')
        btn_delGroup = QtGui.QPushButton('-')
        btn_setPlot = QtGui.QPushButton('*')

        #Setting buttons shape and tooltips
        btn_addGroup.setMaximumWidth(30)
        btn_delGroup.setMaximumWidth(30)
        btn_setPlot.setMaximumWidth(30)
        btn_addGroup.setToolTip('Add a group')
        btn_delGroup.setToolTip('Remove the current group')
        btn_setPlot.setToolTip('Edit plot settings')

        #Conecting buttons
        self.connect(btn_addGroup, QtCore.SIGNAL('clicked()'), toolBox.addTab)
        self.connect(btn_delGroup, QtCore.SIGNAL('clicked()'),
                     toolBox.removeCurrentTab)
        def fun():
            #ternaryData.plot_data([30,30,40])
            ternaryData.add_data(0, [20, 20, 60])
            #ternaryData.set_legend_visibility(0, True)
            #ternaryData.draw()
            
        self.connect(btn_setPlot, QtCore.SIGNAL('clicked()'),
                     fun )
        #TODO: edit_plot
        #self.connect(btn_setPlot, QtCore.SIGNAL('clicked()'), pass)
#        self.connect(self.btn_editGroups, QtCore.SIGNAL('clicked()'),
#                     lambda: PlotSettingsWindow(self, self.TernaryPlot,
#                                                self.canvas).exec_())

        #Buttons layout
        bbox = QtGui.QHBoxLayout()
        bbox.addWidget(btn_addGroup)
        bbox.addWidget(btn_delGroup)
        bbox.addStretch()
        bbox.addWidget(btn_setPlot)
        bbox.setSpacing(2)

        #Main layout
        box = QtGui.QVBoxLayout()
        box.addLayout(bbox)
        box.addWidget(toolBox)
        box.setSpacing(15)
        self.setLayout(box)
        self.setMinimumHeight(400)


class main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setCentralWidget(GroupsFrame(['A', 'B', 'C']))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = main()
    main.show()
    sys.exit(app.exec_())
