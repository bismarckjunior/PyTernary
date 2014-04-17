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


class TernarySettingsFrame(QtGui.QFrame):
    def __init__(self, ternaryData, parent=None):
        super(TernarySettingsFrame, self).__init__(parent)
        self.ternaryData = ternaryData
        self.vars2update = []
        self.create_frame()
        self.set_connections()

    def create_frame(self):
        #Labels
        l_title = QtGui.QLabel()
        l_axesLabel = [QtGui.QLabel() for i in range(3)]
        l_title_size = QtGui.QLabel()
        l_short_size = QtGui.QLabel()
        l_main_size = QtGui.QLabel()

        #Lines edit
        self.le_title = QtGui.QLineEdit()
        self.le_shortLabels = [QtGui.QLineEdit() for i in range(3)]
        self.le_mainLabels = [QtGui.QLineEdit() for i in range(3)]

        #Spinboxes
        self.sb_title = QtGui.QSpinBox()
        self.sb_shortLabels = QtGui.QSpinBox()
        self.sb_mainLabels = QtGui.QSpinBox()

        #Checkboxes
        self.cb_inv = QtGui.QCheckBox()
        self.cb_perc = QtGui.QCheckBox()
        self.cb_grid = QtGui.QCheckBox()
        self.cb_ticks = QtGui.QCheckBox()
        self.cb_min_max = QtGui.QCheckBox()

        #Horizontal boxes
        hbox_title = QtGui.QHBoxLayout()
        hbox_axesLabel = [QtGui.QHBoxLayout() for i in range(3)]
        hbox_label_sizes = QtGui.QHBoxLayout()
        hbox_checkboxes = QtGui.QHBoxLayout()

        #Vertical box
        vbox_labels = QtGui.QVBoxLayout()

        #Editing labels and initializing line edit
        l_title.setText('Title:')
        l_title.setFixedWidth(40)
        l_title_size.setText('Size:')
        self.le_title.setText(self.ternaryData.get_title())
        shortLabels = self.ternaryData.get_short_labels()
        mainLabels = self.ternaryData.get_main_labels()
        l_short_size.setText('Short label size:')
        l_short_size.setFixedWidth(98)
        l_main_size.setText('Main label size:')
        l_main_size.setFixedWidth(80)
        for i in range(3):
            l_axesLabel[i].setText('Axis %d:' % (i+1))
            l_axesLabel[i].setFixedWidth(40)
            self.le_shortLabels[i].setFixedWidth(100)
            self.le_shortLabels[i].setText(shortLabels[i])
            self.le_mainLabels[i].setText(mainLabels[i])

        #Editing spinboxes
        TP = self.ternaryData.ternaryPlot
        fontsizes = []
        for plot in [TP.ttitle, TP.short_labels_plot[0]]:
            if plot:
                font_props = plot.properties()['fontproperties']
                fontsizes.append(int(font_props.get_size_in_points()))
            else:
                fontsizes.append(15)
        plot_long_label = TP.axes[0].plots['label']
        if plot_long_label:
            font_props = plot_long_label[0].properties()['fontproperties']
            fontsizes.append(int(font_props.get_size_in_points()))
        else:
            fontsizes.append(15)

        self.sb_title.setValue(fontsizes.pop(0))
        self.sb_shortLabels.setValue(fontsizes.pop(0))
        self.sb_mainLabels.setValue(fontsizes.pop(0))

        #Editing checkboxes
        self.cb_inv.setText('Inverse')
        self.cb_perc.setText('Percentage')
        self.cb_grid.setText('Grid')
        self.cb_ticks.setText('Ticks')
        self.cb_min_max.setText('Minimum and Maximum values')

        #Editing horizontal boxes
        hbox_title.addWidget(l_title)
        hbox_title.addWidget(self.le_title)
        hbox_title.addWidget(l_title_size)
        hbox_title.addWidget(self.sb_title)
        vbox_labels.addLayout(hbox_title)
        for i in range(3):
            hbox_axesLabel[i].addWidget(l_axesLabel[i])
            hbox_axesLabel[i].addWidget(self.le_shortLabels[i])
            hbox_axesLabel[i].addWidget(self.le_mainLabels[i])
            vbox_labels.addLayout(hbox_axesLabel[i])
        hbox_label_sizes.addWidget(l_short_size)
        hbox_label_sizes.addWidget(self.sb_shortLabels)
        hbox_label_sizes.addSpacing(2)
        hbox_label_sizes.addWidget(l_main_size)
        hbox_label_sizes.addWidget(self.sb_mainLabels)
        hbox_label_sizes.addStretch()

        #vbox_labels.addWidget(self.sb_shortLabels)
        #vbox_labels.addWidget(self.sb_mainLabels)
        vbox_labels.addLayout(hbox_label_sizes)

        hbox_checkboxes.addSpacing(10)
        hbox_checkboxes.addWidget(self.cb_inv)
        hbox_checkboxes.addWidget(self.cb_perc)
        hbox_checkboxes.addWidget(self.cb_min_max)
        hbox_checkboxes.addWidget(self.cb_grid)
        hbox_checkboxes.addWidget(self.cb_ticks)

        #Editing inverse checkbox
        if self.ternaryData.ternaryPlot.inverseOn:
            self.cb_inv.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb_inv.setCheckState(QtCore.Qt.Unchecked)

        #Editing percentage checkbox
        if self.ternaryData.ternaryPlot.axes[0].percentageOn:
            self.cb_perc.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb_perc.setCheckState(QtCore.Qt.Unchecked)

        #Editing min_max checkbox
        if self.ternaryData.ternaryPlot.min_maxOn:
            self.cb_min_max.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb_min_max.setCheckState(QtCore.Qt.Unchecked)

        #Editing grid checkbox
        if self.ternaryData.ternaryPlot.gridOn:
            self.cb_grid.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb_grid.setCheckState(QtCore.Qt.Unchecked)

        #Editing ticks checkbox
        if self.ternaryData.ternaryPlot.ticks_visibility:
            self.cb_ticks.setCheckState(QtCore.Qt.Checked)
        else:
            self.cb_ticks.setCheckState(QtCore.Qt.Unchecked)

        #Group box
        gbox_labels = QtGui.QGroupBox()
        gbox_labels.setTitle(' Labels ')
        gbox_labels.setLayout(vbox_labels)

        #Setting main frame
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(gbox_labels)
        vbox.addLayout(hbox_checkboxes)
        self.setLayout(vbox)

    def set_connections(self):
        #Lines edit connection
        self.le_title.editingFinished.connect(lambda: self.set_data('title'))
        for i in range(3):
            self.le_shortLabels[i].editingFinished.connect(lambda:
                self.set_data('short_labels'))
            self.le_mainLabels[i].editingFinished.connect(lambda:
                self.set_data('main_labels'))

        #Spinboxes connection
        self.sb_title.valueChanged.connect(lambda: self.set_data('title'))
        self.sb_shortLabels.valueChanged.connect(lambda: self.set_data('short_labels'))
        self.sb_mainLabels.valueChanged.connect(lambda: self.set_data('main_labels'))

        #Checkboxes connection
        self.cb_inv.clicked.connect(lambda: self.set_data('inverse'))
        self.cb_perc.clicked.connect(lambda: self.set_data('percentage'))
        self.cb_min_max.clicked.connect(lambda: self.set_data('min_max'))
        self.cb_grid.clicked.connect(lambda: self.set_data('grid'))
        self.cb_ticks.clicked.connect(lambda: self.set_data('ticks'))

    def set_data(self, var):
#        if var not in self.vars2update:
#            self.vars2update.append(var)
#        if key == 'title':
#            d = {'title': self.le_title.text().trimmed(),
#                 'fontsize': self.sb_title.value()}
#            self.new_props[d] = ternaryPlot.set_title
#        elif key == 'short_labels':
#            short_labels = [le.text().trimmed() for le in self.le_shortLabels]
#            self.new_props[ternaryPlot.set_short_labels] = short_labels
#        elif key == 'main_labels':
#            main_labels = [le.text().trimmed() for le in self.le_mainLabels]
#            self.new_props[ternaryPlot.set_main_labels] = main_labels
#        elif key == 'inverse':
#            inverse = self.cb_inv.isChecked()
#            self.new_props[self.ternaryData.set_inverse] = inverse
#        elif key == 'percentage':
#            percentage = self.cb_perc.isChecked()
#            self.new_props[ternaryPlot.percentage] = percentage
#        elif key == 'min_max':
#            min_max = self.cb_min_max.isChecked()
#            self.new_props[ternaryPlot.show_min_max] = min_max
#        elif key == 'grid':
#            grid = self.cb_grid.isChecked()
#            self.new_props[ternaryPlot.grid] = grid
#        elif key == 'ticks':
#            ticks = self.cb_ticks.isChecked()
#            self.new_props[ternaryPlot.set_ticks_visibility] = ticks
        ternaryPlot = self.ternaryData.ternaryPlot
        if var == 'title':
            title = self.le_title.text()
            fontsize = self.sb_title.value()
            ternaryPlot.set_title(title, fontsize=fontsize)
        elif var == 'short_labels':
            short_labels = [le.text().trimmed() for le in self.le_shortLabels]
            fontsize = self.sb_shortLabels.value()
            ternaryPlot.set_short_labels(short_labels, fontsize=fontsize)
        elif var == 'main_labels':
            main_labels = [le.text().trimmed() for le in self.le_mainLabels]
            fontsize = self.sb_mainLabels.value()
            ternaryPlot.set_main_labels(main_labels, fontsize=fontsize)
        elif var == 'inverse':
            inverse = self.cb_inv.isChecked()
            self.ternaryData.set_inverse(inverse)
        elif var == 'percentage':
            percentage = self.cb_perc.isChecked()
            ternaryPlot.percentage(percentage)
        elif var == 'min_max':
            min_max = self.cb_min_max.isChecked()
            ternaryPlot.show_min_max(min_max)
        elif var == 'grid':
            grid = self.cb_grid.isChecked()
            ternaryPlot.grid(grid)
        elif var == 'ticks':
            ticks = self.cb_ticks.isChecked()
            ternaryPlot.set_ticks_visibility(ticks)
        self.ternaryData.draw()

#    def apply_new_props(self):
##        for fun, value in self.new_props.items():
##            if type(fun) == dict:
##                value(**fun)
##            else:
##                fun(value)     
#        ternaryPlot = self.ternaryData.ternaryPlot
#        if 'title' in self.vars2update:
#            title = self.le_title.text()
#            fontsize = self.sb_title.value()
#            ternaryPlot.set_title(title, fontsize=fontsize)
#        if 'short_labels' in self.vars2update:
#            short_labels = [le.text().trimmed() for le in self.le_shortLabels]
#            fontsize = self.sb_shortLabels.value()
#            ternaryPlot.set_short_labels(short_labels, fontsize=fontsize)
#        if 'main_labels' in self.vars2update:
#            main_labels = [le.text().trimmed() for le in self.le_mainLabels]
#            fontsize = self.sb_mainLabels.value()
#            ternaryPlot.set_main_labels(main_labels, fontsize=fontsize)
#        if 'inverse' in self.vars2update:
#            inverse = self.cb_inv.isChecked()
#            self.ternaryData.set_inverse(inverse)
#        if 'percentage' in self.vars2update:
#            percentage = self.cb_perc.isChecked()
#            ternaryPlot.percentage(percentage)
#        if 'min_max' in self.vars2update:
#            min_max = self.cb_min_max.isChecked()
#            ternaryPlot.show_min_max(min_max)
#        if 'grid' in self.vars2update:
#            grid = self.cb_grid.isChecked()
#            ternaryPlot.grid(grid)
#        if 'ticks' in self.vars2update:
#            ticks = self.cb_ticks.isChecked()
#            ternaryPlot.set_ticks_visibility(ticks)


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
#        self.new_props = {}     # New properties for plot
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
        value = str(self.item(row, col).text()).strip()
        if value:
            self.ternaryData.update_properties(row, label=value)
            self.ternaryData.renameGroupHeader(row, value)

    def __comboBox_action(self, row):
        comboBox = self.signalMapperComboBox.mapping(row)
        value = str(comboBox.currentText())
        self.ternaryData.update_properties(row, marker=value)

    def __spinBox_action(self, row):
        spinBox = self.signalMapperSpinBox.mapping(row)
        value = float(spinBox.value())
        self.ternaryData.update_properties(row, markersize=value)

    def __checkBox_legend_action(self, row):
        checkbox_legend = self.signalMapperLegend.mapping(row)
        legend_visible = checkbox_legend.isChecked()
        
        if legend_visible:
            checkBox_plot = self.signalMapperPlot.mapping(row)
            checkBox_plot.setCheckState(QtCore.Qt.Checked)
            self.__checkBox_plot_action(row)
            #self.ternaryData.update_properties(row, visible=True)
        self.ternaryData.set_legend_visibility(row, legend_visible)

    def __checkBox_plot_action(self, row):
        checkbox_plot = self.signalMapperPlot.mapping(row)
        plot_visible = checkbox_plot.isChecked()
#        self.ternaryData.update_properties(row, visible=plot_visible)
        if not plot_visible:
            checkBox_legend = self.signalMapperLegend.mapping(row)
            checkBox_legend.setCheckState(QtCore.Qt.Unchecked)
            self.__checkBox_legend_action(row)
            #self.ternaryData.set_legend_visibility(row, False)
        self.ternaryData.update_properties(row, visible=plot_visible)

    def __setCellColor(self, row, col):
        if col == 1:
            color = QtGui.QColorDialog.getColor()
            if color.isValid():
                self.frmColor[row].setStyleSheet("QWidget {background-color: %s}" % color.name())
                value = str(color.name())
                self.ternaryData.update_properties(row, color=value)


#    def set_new_props(self, row, key=None, value=None):
#        if row not in self.new_props:
#            index = self.ternaryData.groups[row]
#            self.new_props[row] = self.ternaryData.get_plot_properties(index)
#        if key:
#            self.new_props[row][key] = value


class PlotSettingsWindow(QtGui.QDialog):
    def __init__(self, ternaryData, parent=None):
        super(PlotSettingsWindow, self).__init__(parent)
        self.setWindowTitle('Plot Settings')
        self.ternaryData = ternaryData

        self.create_main_frame()

    def create_main_frame(self):
        self.groupsTable = GroupsSettingsTable(self.ternaryData)
        self.ternarySettingsFrame = TernarySettingsFrame(self.ternaryData)

        #Creating main_frame
        mbox = QtGui.QVBoxLayout()
        mbox.addWidget(self.groupsTable)
        mbox.addWidget(self.ternarySettingsFrame)

        self.setLayout(mbox)
        self.setGeometry(QtCore.QRect(10, 50, 490, 350))


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from TernaryPlot import TernaryPlot
    ternaryPlot = TernaryPlot(short_labels=['a','b','c'])
    TD = TernaryData(['S', 'D', 'E'], ternaryPlot, 3)
    TD.add_group()
    #TD.remove_group(0)
    TD.add_group()
    app = QtGui.QApplication(sys.argv)
    main = PlotSettingsWindow(TD)
    main.show()
    app.exec_()
