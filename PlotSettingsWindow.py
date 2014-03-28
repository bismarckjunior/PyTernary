# -*- coding: iso-8859-1 -*-
"""
@author: Bismarck Gomes Souza Junior
@date:   Tue Mar 25 19:41:49 2014
@email:  bismarckjunior@outlook.com
@brief:  Window to edit plot settings.
"""
from PyQt4 import QtGui, QtCore
from TernaryData import TernaryData
import sys


class GroupsSettingsTable(QtGui.QTableWidget):
    ROWHEIGHT = 22
    markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4',
                        's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_']
    def __init__(self, ternaryData, parent=None):
        super(GroupsSettingsTable, self).__init__(parent)
        self.ternaryData = ternaryData
        self.verticalHeader().setVisible(False)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(['Name', 'Color', 'Marker', 'Size',
                                        'Plot', 'Legend'])
        columnsWidth = [150] + [60]*5
        for i, column in enumerate(columnsWidth):
            self.setColumnWidth(i, column)
        
        self.addRows()
        
        #Connections
        self.cellClicked.connect(self.__setCellColor)
        self.cellChanged.connect(self.__groupLabel_action)

    def addRows(self):
        self.frmColor = []      # Frames for color
        self.new_props = {}     # New properties for plot
        self.legends = []       # List of bools for legends plot

        self.signalMapperComboBox = QtCore.QSignalMapper()
        self.signalMapperSpinBox = QtCore.QSignalMapper()
        self.signalMapperPlot = QtCore.QSignalMapper()
        self.signalMapperLegend = QtCore.QSignalMapper()

        for row, index in enumerate(self.ternaryData.groups):
            self.insertRow(row)
            self.setRowHeight(row, self.ROWHEIGHT)
            props = self.ternaryData.get_plot_properties(index)
            props['visible'] = self.ternaryData.get_plot_visibility(index)
            #self.new_props[row] = props

            #Label
            item = QtGui.QTableWidgetItem(props['label'])
            self.setItem(row, 0, item)

            #Color
            color = QtGui.QColor(props['color'])
            self.frmColor.append(QtGui.QFrame())
            self.frmColor[-1].setStyleSheet("QWidget {background-color: %s}" % color.name())
            self.setCellWidget(row, 1, self.frmColor[-1])

            #Marker
            comboBox = QtGui.QComboBox()
            comboBox.addItems(self.markers)
            comboBox.setCurrentIndex(self.markers.index(props['marker']))
            comboBox.currentIndexChanged.connect(self.signalMapperComboBox.map)
            self.signalMapperComboBox.setMapping(comboBox, row)
            self.setCellWidget(row, 2, comboBox)

            #Marker size
            sbox = QtGui.QSpinBox()
            sbox.setValue(props['markersize'])
            sbox.setMinimum(1)
            sbox.setMaximum(30)
            sbox.valueChanged.connect(self.signalMapperSpinBox.map)
            self.signalMapperSpinBox.setMapping(sbox, row)
            self.setCellWidget(row, 3, sbox)

            #Plot
            chkValue = props['visible']
            frame = QtGui.QFrame()
            frame.setStyleSheet("QWidget {background-color: white}")
            chkBoxPlot = QtGui.QCheckBox('')
            chkBoxPlot.setCheckState(QtCore.Qt.Checked if chkValue else QtCore.Qt.Unchecked)
            chkBoxPlot.clicked.connect(self.signalMapperPlot.map)
            self.signalMapperPlot.setMapping(chkBoxPlot, row)
            hbox = QtGui.QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(chkBoxPlot)
            hbox.addStretch(1)
            hbox.setMargin(2)
            frame.setLayout(hbox)
            self.setCellWidget(row, 4, frame)

            #Legend
            chkValue = self.ternaryData.get_legend_visibility(index)
            self.legends.append(chkValue)
            frame = QtGui.QFrame()
            frame.setStyleSheet("QWidget {background-color: white}")
            chkBoxLegend = QtGui.QCheckBox('')
            chkBoxLegend.setCheckState(QtCore.Qt.Checked if chkValue else QtCore.Qt.Unchecked)
            chkBoxLegend.clicked.connect(self.signalMapperLegend.map)
            self.signalMapperLegend.setMapping(chkBoxLegend, row)
            hbox = QtGui.QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(chkBoxLegend)
            hbox.addStretch(1)
            hbox.setMargin(2)
            frame.setLayout(hbox)
            self.setCellWidget(row, 5, frame)

        self.signalMapperComboBox.mapped.connect(self.__comboBox_action)
        self.signalMapperSpinBox.mapped.connect(self.__spinBox_action)
        self.signalMapperPlot.mapped.connect(self.__checkBox_plot_action)
        self.signalMapperLegend.mapped.connect(self.__checkBox_legend_action)

    def __groupLabel_action(self, row, col):
        value = str(self.item(row, col).text())
        self.set_new_props(row, 'label', value)

    def __comboBox_action(self, row):
        comboBox = self.signalMapperComboBox.mapping(row)
        self.set_new_props(row, 'marker', str(comboBox.currentText()))

    def __spinBox_action(self, row):
        spinBox = self.signalMapperSpinBox.mapping(row)
        self.set_new_props(row, 'markersize', float(spinBox.value()))

    def __checkBox_legend_action(self, row):
        checkBox = self.signalMapperLegend.mapping(row)
        self.legends[row] = checkBox.isChecked()
        self.set_new_props(row)

    def __checkBox_plot_action(self, row):
        checkBox = self.signalMapperPlot.mapping(row)
        self.set_new_props(row, 'visible', checkBox.isChecked())

    def __setCellColor(self, row, col):
        if col == 1:
            color = QtGui.QColorDialog.getColor()
            if color.isValid():
                self.frmColor[row].setStyleSheet("QWidget {background-color: %s}" % color.name())
                self.set_new_props(row, 'color', str(color.name()))

    def set_new_props(self, row, key=None, value=None):
        if row not in self.new_props:
            index = self.ternaryData.groups[row]
            self.new_props[row] = self.ternaryData.get_plot_properties(index)
        if key and value:
            self.new_props[row][key] = value


class PlotSettingsWindow(QtGui.QDialog):
    def __init__(self, ternaryData, parent=None):
        super(PlotSettingsWindow, self).__init__(parent)
        self.setWindowTitle('Plot Settings')
        self.ternaryData = ternaryData

        self.create_main_frame()

    def create_main_frame(self):
        self.groupsTable = GroupsSettingsTable(self.ternaryData)

        #Creating Ok button
        btn_ok = QtGui.QPushButton('Ok')
        btn_cancel = QtGui.QPushButton('Cancel')
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(btn_ok)
        hbox.addWidget(btn_cancel)

        #Conecting
        self.connect(btn_ok, QtCore.SIGNAL('clicked()'), self.__okAction)
        self.connect(btn_cancel, QtCore.SIGNAL('clicked()'),
                     self.__cancelAction)

        #Creating main_frame
        mbox = QtGui.QVBoxLayout()
        mbox.addWidget(self.groupsTable)
        mbox.addLayout(hbox)
        self.setLayout(mbox)
        self.setGeometry(QtCore.QRect(10, 50, 490, 350))

    def __cancelAction(self):
        self.reject()
    
    def __okAction(self):
        for key, props in self.groupsTable.new_props.items():
            index = self.ternaryData.groups[key]
            self.ternaryData.update_properties(index, **props)
            legend = self.groupsTable.legends[key]
            self.ternaryData.set_legend_visibility(index, legend)
            self.ternaryData.renameGroupHeader(index, props['label'])
        self.accept()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from TernaryPlot import TernaryPlot
    ternaryPlot = TernaryPlot()
    TD = TernaryData(['S', 'D', 'E'], ternaryPlot, 3)
    TD.add_group()
    TD.add_group()
    app = QtGui.QApplication(sys.argv)
    main = PlotSettingsWindow(TD)
    main.show()
    app.exec_()
