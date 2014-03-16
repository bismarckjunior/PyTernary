# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Sun Mar 16 09:19:06 2014
@email:  bismarckjunior@outlook.com
@brief:  Table of data
"""
from PyQt4 import QtGui, QtCore
import sys


class TableData(QtGui.QTableWidget):
    ROWHEIGHT = 25

    def __init__(self, headersLabel, nrow, ncol, parent=None):
        super(TableData, self).__init__(nrow, ncol, parent)
        self.headersLabel = headersLabel
        self.ncol = ncol
        self.setHorizontalHeaderLabels(headersLabel)
        header = self.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)

        #Inserting vertical headers and setting row heights
        self.__updateRows()

        #Connections
        header.sectionDoubleClicked.connect(self.__changeHeaderItem)
        self.cellChanged.connect(self.__cellTableChanged)

        #Edit with oneclick
        #self.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)

    def __changeHeaderItem(self, index):
        oldHeader = self.horizontalHeaderItem(index).text()
        newHeader, ok = QtGui.QInputDialog.getText(self,
                                                   'Change Header Label',
                                                   'Header:',
                                                   QtGui.QLineEdit.Normal,
                                                   oldHeader)
        if ok:
            self.headersLabel[index] = newHeader
            self.horizontalHeaderItem(index).setText(newHeader)

    def __emptyCell(self, row, col):
        'Boole for empty cell.'
        item = self.item(row, col)
        if item and item.text():
            return False
        else:
            return True

    def __emptyRow(self, row, colmax=None):
        'Bool for empty row.'
        colmax = colmax if colmax else self.ncol
        for col in range(colmax):
            if not self.__emptyCell(row, col):
                return False
        return True

    def __addRow(self, row=None):
        row = self.rowCount() if not row else row+1
        if not self.__emptyRow(row-1):
            self.insertRow(row)
            self.setRowHeight(row, self.ROWHEIGHT)
            self.setVerticalHeaderItem(row,
                                       QtGui.QTableWidgetItem('%02i' % (row+1)))
        #self.setCurrentCell(row, 0)

    def __updateRows(self):
        header = ['%02i' % (i+1) for i in range(self.rowCount())]
        self.setVerticalHeaderLabels(header)
        for i in range(self.rowCount()):
            self.setRowHeight(i, self.ROWHEIGHT)

    def __cellTableChanged(self, row, col):
        item = self.item(row, col)
        text = item.text().replace(',', '.')
        try:
            value = float(text)
            self.__addRow()
            item.setText('%.2f' % value)
        except ValueError:
            item.setText('')
            self.setCurrentCell(row, col)
        if col == self.ncol-1 and self.__emptyRow(row, col):
            self.setCurrentCell(row+1, 0)

    def keyPressEvent(self, event):
        row = self.currentRow()
        col = self.currentColumn()
        if (event.key() == QtCore.Qt.Key_Return):
            #Return key
            if col < self.ncol-1:
                self.setCurrentCell(row, col+1)
            elif self.__emptyRow(row):
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
            nrow = self.rowCount()
            if nrow > 1:
                for row in range(nrow-1)[::-1]:
                    if row in tmp and tmp[row] == 3:
                            self.removeRow(row)
                row = nrow-2
                while(row >= 0):
                    if self.__emptyRow(row) and self.__emptyRow(row+1):
                        self.removeRow(row)
                    row -= 1

                self.__updateRows()
        else:
            QtGui.QTableView.keyPressEvent(self, event)


class TernaryTableData(QtGui.QTableWidget):
    ROWHEIGHT = 25

    def __init__(self, headers, dataWidget=None, parent=None):
        super(TableData, self).__init__(parent)
        self.dataWidget = dataWidget
        self.setRowCount(1)
        self.setColumnCount(3)
        #TODO: dataWidget.headers()
        self.setHorizontalHeaderLabels(headers)
        header = self.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)
        header.sectionDoubleClicked.connect(self.__changeHeaderItem)
        self.removeRow(0)
        self.__addRow()

        #Connections
        self.cellChanged.connect(self.__cellTableChanged)

        #Edit with oneclick
        #self.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)

    def __changeHeaderItem(self, index):
        oldHeader = self.horizontalHeaderItem(index).text()
        newHeader, ok = QtGui.QInputDialog.getText(self,
                                                   'Change Header Label',
                                                   'Header:',
                                                   QtGui.QLineEdit.Normal,
                                                   oldHeader)
        if ok:
            self.dataWidget.shortTitles[index] = newHeader
            #TODO: dataWidget
            for table in [group['table'] for group in self.dataWidget.groups]:
                table.horizontalHeaderItem(index).setText(newHeader)

    def __addRow(self, row=None):
        row = self.rowCount() if not row else row+1
        self.insertRow(row)
        self.setRowHeight(row, self.ROWHEIGHT)
        self.setVerticalHeaderItem(row,
                                   QtGui.QTableWidgetItem('%02i' % (row+1)))
        self.setCurrentCell(row, 0)

    def __updateRows(self):
        header = ['%02i' % (i+1) for i in range(self.rowCount())]
        self.setVerticalHeaderLabels(header)

    def __cellTableChanged(self, row, col):
        text = self.item(row, col).text().replace(',', '.')
        try:
            value = float(text)
            self.item(row, col).setText('%.2f' % value)

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
                if sum_ <= 1:
                    value = 1. - sum_
                elif sum_ <= 100:
                    value = 100. - sum_
                else:
                    value = ''
                if i != col:
                    item = QtGui.QTableWidgetItem(str(value))
                    self.setItem(row, i, item)
                    self.setCurrentCell(row, i)
            #TODO: update_plot

        except ValueError:
            pass

    def keyPressEvent(self, event):
        row = self.currentRow()
        col = self.currentColumn()
        if (event.key() == QtCore.Qt.Key_Return):
            if col < 2:
                self.setCurrentCell(row, col+1)
            elif col == 2 and row == self.rowCount()-1:
                for i in range(3):
                    item = self.item(row, i)
                    if item or (item and item.text()):
                        self.__addRow()
                        break
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
                        #TODO: update_plot
                self.__updateRows()
        else:
            QtGui.QTableView.keyPressEvent(self, event)

class main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        
        table = TableData(['A', 'B', 'C'], 1, 3)
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
    