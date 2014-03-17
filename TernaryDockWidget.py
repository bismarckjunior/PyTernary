# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sun Mar 16 20:08:55 2014
@email:  bismarckjunior@outlook.com
@brief:  
"""
from PyQt4 import QtGui, QtCore
from TernaryTableData import TernaryTableData
import sys


class TabFrame(QtGui.QFrame):
    FORMATFILE = '.dat'

    def __init__(self, headerLabels, parent=None):
        super(TabFrame, self).__init__(parent)
        self.headerLabels = headerLabels
        self.table = TernaryTableData(self.headerLabels)

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
                    print row
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
            lines_error = ['4','5']
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


class TernaryToolBox(QtGui.QToolBox):
    def __init__(self, headerLabels, parent=None):
        super(TernaryToolBox, self).__init__(parent)
        self.headerLabels = headerLabels
        self.setMaximumWidth(300)
        self.addTab()

    def addTab(self):
        #Updating max tab number
        if self.count() == 0:
            print 'ok'
            self.maxTabNumber = 0
        self.maxTabNumber += 1

        frame = TabFrame(self.headerLabels)
        TabName = 'Group %d' % self.maxTabNumber
        self.addItem(frame, TabName)
        self.setCurrentIndex(self.count()-1)

    def removeCurrentTab(self):
        self.removeTab(self.currentIndex())

    def removeTab(self, index):
        if self.count() == 1:
            return
        if index == self.count()-1:
            self.maxTabNumber -= 1
        self.removeItem(index)
        self.setCurrentIndex(index-1)
        #TODO: update_plot


class main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        #frame = TabFrame(['A', 'B', 'C'])
        
        #Buttons
        btn_add = QtGui.QPushButton('+')
        btn_del = QtGui.QPushButton('-')
        
        toolBox = TernaryToolBox(['A', 'B', 'C'])
        box = QtGui.QVBoxLayout()
        box.addWidget(btn_add)
        box.addWidget(btn_del)
        box.addWidget(toolBox)
        frame = QtGui.QFrame()
        frame.setLayout(box)
        self.setCentralWidget(frame)
        
        #Connecting
        self.connect(btn_add, QtCore.SIGNAL('clicked()'), toolBox.addTab)
        self.connect(btn_del, QtCore.SIGNAL('clicked()'), toolBox.removeCurrentTab)
        




class TernaryDockWidget(QtGui.QDockWidget):
    pass






if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = main()
    main.show()
    sys.exit(app.exec_())
