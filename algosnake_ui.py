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
        self.game_grid.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.game_grid.setGridStyle(QtCore.Qt.SolidLine)
        self.game_grid.setCornerButtonEnabled(False)
        self.game_grid.setRowCount(26)
        self.game_grid.setColumnCount(37)
        self.game_grid.setObjectName(_fromUtf8("game_grid"))
        self.game_grid.horizontalHeader().setVisible(False)
        self.game_grid.horizontalHeader().setDefaultSectionSize(26)
        self.game_grid.horizontalHeader().setMinimumSectionSize(25)
        self.game_grid.verticalHeader().setVisible(False)
        self.game_grid.verticalHeader().setDefaultSectionSize(26)
        self.game_grid.verticalHeader().setMinimumSectionSize(25)
        self.gridLayout.addWidget(self.game_grid, 0, 0, 1, 1)
        self.button_box = QtGui.QFrame(self.centralwidget)
        self.button_box.setGeometry(QtCore.QRect(785, 782, 221, 46))
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
        self.stop_button.setEnabled(False)
        self.stop_button.setObjectName(_fromUtf8("stop_button"))
        self.horizontalLayout.addWidget(self.stop_button)
        self.reset_button = QtGui.QPushButton(self.button_box)
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.horizontalLayout.addWidget(self.reset_button)
        self.speed_selector = QtGui.QSpinBox(self.centralwidget)
        self.speed_selector.setGeometry(QtCore.QRect(730, 795, 42, 22))
        self.speed_selector.setMinimum(1)
        self.speed_selector.setMaximum(20)
        self.speed_selector.setObjectName(_fromUtf8("speed_selector"))
        self.speed_label = QtGui.QLabel(self.centralwidget)
        self.speed_label.setGeometry(QtCore.QRect(685, 800, 41, 16))
        self.speed_label.setObjectName(_fromUtf8("speed_label"))
        self.num_found_label = QtGui.QLabel(self.centralwidget)
        self.num_found_label.setGeometry(QtCore.QRect(75, 823, 46, 13))
        self.num_found_label.setObjectName(_fromUtf8("num_found_label"))
        self.found_separator = QtGui.QFrame(self.centralwidget)
        self.found_separator.setGeometry(QtCore.QRect(35, 814, 106, 10))
        self.found_separator.setFrameShape(QtGui.QFrame.HLine)
        self.found_separator.setFrameShadow(QtGui.QFrame.Raised)
        self.found_separator.setLineWidth(2)
        self.found_separator.setObjectName(_fromUtf8("found_separator"))
        self.num_found_indicator = QtGui.QLabel(self.centralwidget)
        self.num_found_indicator.setGeometry(QtCore.QRect(35, 778, 111, 36))
        self.num_found_indicator.setObjectName(_fromUtf8("num_found_indicator"))
        self.algoList = QtGui.QListWidget(self.centralwidget)
        self.algoList.setGeometry(QtCore.QRect(435, 740, 216, 126))
        self.algoList.setObjectName(_fromUtf8("algoList"))
        self.time_label = QtGui.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(211, 824, 46, 13))
        self.time_label.setObjectName(_fromUtf8("time_label"))
        self.time_separator = QtGui.QFrame(self.centralwidget)
        self.time_separator.setGeometry(QtCore.QRect(171, 815, 106, 10))
        self.time_separator.setFrameShape(QtGui.QFrame.HLine)
        self.time_separator.setFrameShadow(QtGui.QFrame.Raised)
        self.time_separator.setLineWidth(2)
        self.time_separator.setObjectName(_fromUtf8("time_separator"))
        self.time_indicator = QtGui.QLabel(self.centralwidget)
        self.time_indicator.setGeometry(QtCore.QRect(166, 779, 116, 36))
        self.time_indicator.setObjectName(_fromUtf8("time_indicator"))
        self.moves_label = QtGui.QLabel(self.centralwidget)
        self.moves_label.setGeometry(QtCore.QRect(344, 824, 46, 13))
        self.moves_label.setObjectName(_fromUtf8("moves_label"))
        self.moves_indicator = QtGui.QLabel(self.centralwidget)
        self.moves_indicator.setGeometry(QtCore.QRect(301, 779, 116, 36))
        self.moves_indicator.setObjectName(_fromUtf8("moves_indicator"))
        self.moves_separator = QtGui.QFrame(self.centralwidget)
        self.moves_separator.setGeometry(QtCore.QRect(306, 815, 106, 10))
        self.moves_separator.setFrameShape(QtGui.QFrame.HLine)
        self.moves_separator.setFrameShadow(QtGui.QFrame.Raised)
        self.moves_separator.setLineWidth(2)
        self.moves_separator.setObjectName(_fromUtf8("moves_separator"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.speed_label.setBuddy(self.speed_selector)
        
        self.retranslateUi(MainWindow)
        
        self.MainWindow = MainWindow
        
        #Connections
        QtCore.QObject.connect(self.game_grid, QtCore.SIGNAL(_fromUtf8("cellClicked(int, int)")), self.ui_functions.itemClicked)
        QtCore.QObject.connect(self.start_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.startButtonPressed)
        QtCore.QObject.connect(self.stop_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.stopbuttonPressed)
        QtCore.QObject.connect(self.reset_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.resetGrid)
        QtCore.QObject.connect(MainWindow, QtCore.SIGNAL("snakeMoved"), self.ui_functions.incrementMoveCount)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #Set up the grid
        self.ui_functions.resetGrid()
        
        #Set up algo list
        self.setupAlgos()
        
    def setupAlgos(self):
        item3 = QtGui.QListWidgetItem()
        item3.setText(_translate("MainWindow", "Random", None))
        self.algoList.addItem(item3)
        item3 = QtGui.QListWidgetItem()
        item3.setText(_translate("MainWindow", "Random - Prefer Unexplored", None))
        self.algoList.addItem(item3)
        item4 = QtGui.QListWidgetItem()
        item4.setText(_translate("MainWindow", "Random - Prefer Unexplored Nonstick", None))
        self.algoList.addItem(item4)
        #item1 = QtGui.QListWidgetItem()
        #item1.setText(_translate("MainWindow", "Right Follow (NOT IMPLEMENTED)", None))
        #self.algoList.addItem(item1)
        #item2 = QtGui.QListWidgetItem()
        #item2.setText(_translate("MainWindow", "Left Follow (NOT IMPLEMENTED)", None))
        #self.algoList.addItem(item2)

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
        self.moves_label.setText(_translate("MainWindow", "MOVES", None))
        self.moves_indicator.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">_MOVES_</span></p></body></html>", None))