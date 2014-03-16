# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sun Mar 16 20:08:55 2014
@email:  bismarckjunior@outlook.com
@brief:  
"""
from PyQt4 import QtGui, QtCore


class TabFrame(QtGui.QFrame):
    FORMATFILE = '.dat'

    def __init__(self, dataWidget=None, parent=None):
        super(TabFrame, self).__init__(parent)
        #TODO: dataWidget
        self.headers = dataWidget
        self.table = TernaryTableData(self.headers)

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
                    nrow = self.table.rowCount()
                    self.table.insertRow(nrow)
                    for col in range(3):
                        cell = row[col] if row[col] != '-' else ''
                        self.table.setItem(nrow, col,
                                           QtGui.QTableWidgetItem(cell))
                else:
                    lines_error.append(str(nline+1))

        self.table.insertRow(nrow+1)
        #TODO: update_plot

        #Warning Message
        if lines_error:
            wm = QtGui.QMessageBox(self)
            wm.setWindowTitle('Warning')
            msg = '''<h2 align="center">Warning</h2>
                     <p>Problems in line(s): %s</p>'''
            if len(lines_error) > 5:
                lines_error = lines_error[:5]+['...']
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
        f.write('#%s\t%s\t%s\n' % tuple([h for h in self.headers]))
        for row in range(self.table.rowCount()):
            for col in range(3):
                item = self.table.item(row, col) 
                f.write('%s\t' % (item.text() if item and item.text() else '-'))
            f.write('\n')
        f.close()


class TernaryToolBox(QtGui.QToolBox):
    def __init__(self, parent=None):
        super(TernaryToolBox, self).__init__(parent)
