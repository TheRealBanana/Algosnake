# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'algosnake_ui.ui'
#
# Created: Fri Jan 20 11:56:38 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from algosnake_ui_functions import uiFunctions

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Algosnake_MainWindow(object):
    def setupUi(self, MainWindow):
        self.ui_functions = uiFunctions(self)
        
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1042, 878)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.game_grid_frame = QtGui.QFrame(self.centralwidget)
        self.game_grid_frame.setGeometry(QtCore.QRect(25, 25, 991, 706))
        self.game_grid_frame.setMinimumSize(QtCore.QSize(991, 706))
        self.game_grid_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.game_grid_frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.game_grid_frame.setObjectName(_fromUtf8("game_grid_frame"))
        self.gridLayout = QtGui.QGridLayout(self.game_grid_frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.game_grid = QtGui.QTableWidget(self.game_grid_frame)
        self.game_grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.game_grid.setTabKeyNavigation(False)
        self.game_grid.setProperty("showDropIndicator", False)
        self.game_grid.setDragDropOverwriteMode(False)
        self.game_grid.setAlternatingRowColors(False)
        self.game_grid.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.game_grid.setGridStyle(QtCore.Qt.SolidLine)
        self.game_grid.setCornerButtonEnabled(False)
        self.game_grid.setRowCount(26)
        self.game_grid.setColumnCount(37)
        self.game_grid.setObjectName(_fromUtf8("game_grid"))
        self.game_grid.horizontalHeader().setVisible(False)
        self.game_grid.horizontalHeader().setDefaultSectionSize(26)
        self.game_grid.horizontalHeader().setMinimumSectionSize(26)
        self.game_grid.verticalHeader().setVisible(False)
        self.game_grid.verticalHeader().setDefaultSectionSize(26)
        self.game_grid.verticalHeader().setMinimumSectionSize(26)
        self.gridLayout.addWidget(self.game_grid, 0, 0, 1, 1)
        self.button_box = QtGui.QFrame(self.centralwidget)
        self.button_box.setGeometry(QtCore.QRect(770, 752, 221, 46))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setMinimumSize(QtCore.QSize(0, 0))
        self.button_box.setFrameShape(QtGui.QFrame.StyledPanel)
        self.button_box.setFrameShadow(QtGui.QFrame.Raised)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.button_box)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.start_button = QtGui.QPushButton(self.button_box)
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.horizontalLayout.addWidget(self.start_button)
        self.stop_button = QtGui.QPushButton(self.button_box)
        self.stop_button.setObjectName(_fromUtf8("stop_button"))
        self.horizontalLayout.addWidget(self.stop_button)
        self.reset_button = QtGui.QPushButton(self.button_box)
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.horizontalLayout.addWidget(self.reset_button)
        self.speedSelector = QtGui.QSpinBox(self.centralwidget)
        self.speedSelector.setValue(5)
        self.speedSelector.setGeometry(QtCore.QRect(715, 765, 42, 22))
        self.speedSelector.setObjectName(_fromUtf8("spinBox"))
        self.speed_label = QtGui.QLabel(self.centralwidget)
        self.speed_label.setGeometry(QtCore.QRect(670, 770, 41, 16))
        self.speed_label.setObjectName(_fromUtf8("speed_label"))
        self.num_found_label = QtGui.QLabel(self.centralwidget)
        self.num_found_label.setGeometry(QtCore.QRect(75, 805, 46, 13))
        self.num_found_label.setObjectName(_fromUtf8("num_found_label"))
        self.found_separator = QtGui.QFrame(self.centralwidget)
        self.found_separator.setGeometry(QtCore.QRect(35, 796, 106, 10))
        self.found_separator.setFrameShape(QtGui.QFrame.HLine)
        self.found_separator.setFrameShadow(QtGui.QFrame.Raised)
        self.found_separator.setLineWidth(2)
        self.found_separator.setObjectName(_fromUtf8("found_separator"))
        self.num_found_indicator = QtGui.QLabel(self.centralwidget)
        self.num_found_indicator.setGeometry(QtCore.QRect(35, 760, 111, 36))
        self.num_found_indicator.setObjectName(_fromUtf8("num_found_indicator"))
        self.algoList = QtGui.QListWidget(self.centralwidget)
        self.algoList.setGeometry(QtCore.QRect(470, 740, 181, 91))
        self.algoList.setObjectName(_fromUtf8("listWidget"))
        self.time_label = QtGui.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(220, 805, 46, 13))
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.time_separator = QtGui.QFrame(self.centralwidget)
        self.time_separator.setGeometry(QtCore.QRect(180, 796, 106, 10))
        self.time_separator.setFrameShape(QtGui.QFrame.HLine)
        self.time_separator.setFrameShadow(QtGui.QFrame.Raised)
        self.time_separator.setLineWidth(2)
        self.time_separator.setObjectName(_fromUtf8("time_separator"))
        self.time_indicator = QtGui.QLabel(self.centralwidget)
        self.time_indicator.setGeometry(QtCore.QRect(175, 760, 116, 36))
        self.time_indicator.setObjectName(_fromUtf8("time_indicator"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1042, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.speed_label.setBuddy(self.speedSelector)
        
        self.retranslateUi(MainWindow)
        
        #Connections
        QtCore.QObject.connect(self.game_grid, QtCore.SIGNAL(_fromUtf8("cellClicked(int, int)")), self.ui_functions.itemClicked)
        QtCore.QObject.connect(self.start_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.startButtonPressed)
        QtCore.QObject.connect(self.stop_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.stopbuttonPressed)
        QtCore.QObject.connect(self.reset_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.resetGrid)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #Set up the grid
        self.ui_functions.resetGrid()
        
        #Set up algo list
        self.setupAlgos()
        
    def setupAlgos(self):
        item1 = QtGui.QListWidgetItem()
        item1.setText(_translate("MainWindow", "Right Follow", None))
        self.algoList.addItem(item1)
        item2 = QtGui.QListWidgetItem()
        item2.setText(_translate("MainWindow", "Left Follow", None))
        self.algoList.addItem(item2)
        item3 = QtGui.QListWidgetItem()
        item3.setText(_translate("MainWindow", "Random", None))
        self.algoList.addItem(item3)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.start_button.setText(_translate("MainWindow", "Start", None))
        self.stop_button.setText(_translate("MainWindow", "Stop", None))
        self.reset_button.setText(_translate("MainWindow", "Reset", None))
        self.speed_label.setText(_translate("MainWindow", "Speed:", None))
        self.num_found_label.setText(_translate("MainWindow", "FOUND", None))
        self.num_found_indicator.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">_NUM_FOUND_</span></p></body></html>", None))
        __sortingEnabled = self.algoList.isSortingEnabled()
        self.algoList.setSortingEnabled(False)
        
        self.algoList.setSortingEnabled(__sortingEnabled)
        self.time_label.setText(_translate("MainWindow", "TIME", None))
        self.time_indicator.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">_TIME_</span></p></body></html>", None))
