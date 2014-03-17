# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sun Mar 16 09:19:06 2014
@email:  bismarckjunior@outlook.com
@brief:  Table of data for Ternary plot.
"""
from PyQt4 import QtGui, QtCore
import sys


class EditableHeaderMixin():
    '''This class makes the header of TableData class editable.'''
    def __init__(self):
        self.__modifyHorizontalHeader()

    def __modifyHorizontalHeader(self):
        header = self.horizontalHeader()
        self.line = QtGui.QLineEdit(parent=header.viewport())
        self.line.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.line.setHidden(True)

        #Connecting
        header.sectionDoubleClicked.connect(self.__editHeader)
        self.line.editingFinished.connect(self.__doneEditing)

    def __editHeader(self, index):
        header = self.horizontalHeader()
        edit_geometry = self.line.geometry()
        edit_geometry.setWidth(header.sectionSize(index))
        edit_geometry.moveLeft(header.sectionViewportPosition(index))
        self.line.setGeometry(edit_geometry)
        self.line.setText(self.headerLabels[index])
        self.line.setHidden(False)
        self.line.blockSignals(False)
        self.line.setFocus()
        self.line.selectAll()
        self.index = index

    def __doneEditing(self):
        self.line.blockSignals(True)
        self.line.setHidden(True)
        newHeader = str(self.line.text())
        self.horizontalHeaderItem(self.index).setText(newHeader)
        self.line.setText('')
        self.setCurrentIndex(QtCore.QModelIndex())

#    def __changeHeaderItem(self, index):
#        oldHeader = self.horizontalHeaderItem(index).text()
#        newHeader, ok = QtGui.QInputDialog.getText(self,
#                                                   'Change Header Label',
#                                                   'Header:',
#                                                   QtGui.QLineEdit.Normal,
#                                                   oldHeader)
#        if ok:
#            self.headerLabels[index] = newHeader
#            self.horizontalHeaderItem(index).setText(newHeader)


class TableDataBase(QtGui.QTableWidget):
    ROWHEIGHT = 25

    def __init__(self, nrow, ncol, headerLabels, parent=None):
        super(TableDataBase, self).__init__(nrow, ncol, parent)
        self.headerLabels = headerLabels
        self.ncol = ncol
        self.setHorizontalHeaderLabels(headerLabels)

        header = self.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)

        #Inserting vertical headers and setting row heights
        self.updateRows()

        #Connections
        self.cellChanged.connect(self.__cellTableChanged)

        #Edit with oneclick
        #self.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)

    def isEmptyCell(self, row, col):
        'Boole for empty cell.'
        item = self.item(row, col)
        if item and item.text():
            return False
        else:
            return True

    def isEmptyRow(self, row, colmax=None):
        'Bool for empty row.'
        colmax = colmax if colmax else self.ncol
        for col in range(colmax):
            if not self.isEmptyCell(row, col):
                return False
        return True

    def addRow(self, row=None):
        row = self.rowCount() if not row else row+1
        if not self.isEmptyRow(row-1):
            self.insertRow(row)
            self.setRowHeight(row, self.ROWHEIGHT)
            self.setVerticalHeaderItem(row,
                                       QtGui.QTableWidgetItem('%02i' % (row+1)))
        #self.setCurrentCell(row, 0)

    def updateRows(self):
        header = ['%02i' % (i+1) for i in range(self.rowCount())]
        self.setVerticalHeaderLabels(header)
        for i in range(self.rowCount()):
            self.setRowHeight(i, self.ROWHEIGHT)

    def __cellTableChanged(self, row, col):
        item = self.item(row, col)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        text = item.text().replace(',', '.')
        try:
            value = float(text)
            self.addRow()
            item.setText('%.2f' % value)
        except ValueError:
            item.setText('')
            self.setCurrentCell(row, col)
        if col == self.ncol-1 and self.isEmptyRow(row, col):
            self.setCurrentCell(row+1, 0)

    def keyPressEvent(self, event):
        row = self.currentRow()
        col = self.currentColumn()
        if (event.key() == QtCore.Qt.Key_Return):
            #Return key
            if col < self.ncol-1:
                self.setCurrentCell(row, col+1)
            elif self.isEmptyRow(row):
                self.setCurrentCell(row, 0)
            else:
                self.setCurrentCell(row+1, 0)
        elif(event.key() == QtCore.Qt.Key_Delete):
            #Deleting items
            indexes = self.selectedIndexes()
            tmp = {}
            for index in indexes:
                row = index.row()
                col = index.column()
                self.setItem(row, col, QtGui.QTableWidgetItem())
                tmp[row] = tmp.get(row, 0)+1

            #Deleting lines
            if self.rowCount() > 1:
                for row in range(self.rowCount()-1)[::-1]:
                    if row in tmp and tmp[row] == 3:
                            self.removeRow(row)
                row = self.rowCount()-2
                while(row >= 0):
                    if self.isEmptyRow(row) and self.isEmptyRow(row+1):
                        self.removeRow(row)
                    row -= 1
                self.updateRows()
        else:
            QtGui.QTableView.keyPressEvent(self, event)


class TableData(TableDataBase, EditableHeaderMixin):
    def __init__(self, nrow, ncol, headerLabels, parent=None):
        super(TableData, self).__init__(nrow, ncol, headerLabels, parent)
        EditableHeaderMixin.__init__(self)


class TernaryTableData(TableData):
    ROWSUM = 100

    def __init__(self, headerLabels, dataWidget=None, parent=None):
        super(TernaryTableData, self).__init__(1, 3, headerLabels, parent)
        self.dataWidget = dataWidget

        #Connections
        headers = self.horizontalHeader()
        headers.sectionDoubleClicked.connect(self.__changeHeaderItem)
        self.cellChanged.connect(self.__cellTableChanged)

    def __changeHeaderItem(self, index):
        #TODO: dataWidget
        pass

    def __cellTableChanged(self, row, col):
        line = []
        for i in range(3):
            item = self.item(row, i)
            value = float(item.text()) if item and item.text() else None
            line.append(value)

        #Completing line
        if line.count(None) == 1:
            i = line.index(None)
            line.remove(None)
            sum_ = sum(line)
            if sum_ <= self.ROWSUM:
                value = self.ROWSUM - sum_
            else:
                value = ''
            if i != col:
                item = QtGui.QTableWidgetItem(str(value))
                self.setItem(row, i, item)
                self.setCurrentCell(row, i)


class main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        table = TernaryTableData(['A', 'B', 'C'])
        box = QtGui.QVBoxLayout()
        box.addWidget(table)
        frame = QtGui.QFrame()
        frame.setLayout(box)
        self.setCentralWidget(frame)
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    main = main()
    main.show()
    sys.exit(app.exec_())
    