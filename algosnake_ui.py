# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'algosnake_ui.ui'
#
# Created: Fri Jan 20 11:56:38 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from algosnake_ui_functions import uiFunctions
from minigame import MiniGame

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
        MainWindow.resize(1042, 897)
        MainWindow.setMinimumSize(QtCore.QSize(1042, 897))
        MainWindow.setMaximumSize(QtCore.QSize(1042, 897))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.game_grid_frame = QtGui.QFrame(self.centralwidget)
        self.game_grid_frame.setGeometry(QtCore.QRect(25, 15, 991, 706))
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
        self.button_box.setGeometry(QtCore.QRect(795, 760, 216, 86))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setMinimumSize(QtCore.QSize(0, 0))
        self.button_box.setFrameShape(QtGui.QFrame.StyledPanel)
        self.button_box.setFrameShadow(QtGui.QFrame.Raised)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.gridLayout_2 = QtGui.QGridLayout(self.button_box)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.reset_button = QtGui.QPushButton(self.button_box)
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.gridLayout_2.addWidget(self.reset_button, 3, 0, 1, 1)
        self.clear_button = QtGui.QPushButton(self.button_box)
        self.clear_button.setObjectName(_fromUtf8("clear_button"))
        self.gridLayout_2.addWidget(self.clear_button, 3, 1, 1, 1)
        self.start_button = QtGui.QPushButton(self.button_box)
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.gridLayout_2.addWidget(self.start_button, 2, 0, 1, 1)
        self.stop_button = QtGui.QPushButton(self.button_box)
        self.stop_button.setEnabled(False)
        self.stop_button.setObjectName(_fromUtf8("stop_button"))
        self.gridLayout_2.addWidget(self.stop_button, 2, 1, 1, 1)
        self.speed_selector = QtGui.QSpinBox(self.centralwidget)
        self.speed_selector.setGeometry(QtCore.QRect(730, 795, 42, 22))
        self.speed_selector.setMinimum(1)
        self.speed_selector.setMaximum(28)
        self.speed_selector.setProperty("value", 10)
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
        self.algoList.setGeometry(QtCore.QRect(435, 735, 236, 126))
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
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1042, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menuBar)
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName(_fromUtf8("action_Open"))
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setObjectName(_fromUtf8("action_Save"))
        self.action_minigame = QtGui.QAction(MainWindow)
        self.action_minigame.setObjectName(_fromUtf8("action_minigame"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_minigame)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Quit)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.speed_label.setBuddy(self.speed_selector)
        
        self.retranslateUi(MainWindow)
        
        self.MainWindow = MainWindow
        
        #Connections
        QtCore.QObject.connect(self.game_grid, QtCore.SIGNAL(_fromUtf8("cellClicked(int, int)")), self.ui_functions.itemClicked)
        QtCore.QObject.connect(self.start_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.startButtonPressed)
        QtCore.QObject.connect(self.stop_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.stopButtonPressed)
        QtCore.QObject.connect(self.reset_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.reloadGrid)
        QtCore.QObject.connect(self.clear_button, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ui_functions.resetGrid)
        QtCore.QObject.connect(self.action_Open, QtCore.SIGNAL(_fromUtf8("triggered()")), self.ui_functions.loadGrid)
        QtCore.QObject.connect(self.action_Save, QtCore.SIGNAL(_fromUtf8("triggered()")), self.ui_functions.saveGrid)
        QtCore.QObject.connect(self.action_minigame, QtCore.SIGNAL(_fromUtf8("triggered()")), self.loadSnakeMinigame)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), self.ui_functions.stopAndQuit)
        QtCore.QObject.connect(self.speed_selector, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ui_functions.updateSpeed)
        QtCore.QObject.connect(self.MainWindow, QtCore.SIGNAL("appClosing"), self.ui_functions.stopAndQuit)
        QtCore.QObject.connect(self.MainWindow, QtCore.SIGNAL("snakeMoved"), self.ui_functions.incrementMoveCount)
        QtCore.QObject.connect(self.MainWindow, QtCore.SIGNAL("unlockGrid"), self.ui_functions.unlockGrid)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #Set up the grid
        self.ui_functions.resetGrid()
        
        #Set up algo list
        self.setupAlgos()
        
    def addAlgo(self, text):
        new_item = QtGui.QListWidgetItem()
        new_item.setText(_translate("MainWindow", text, None))
        self.algoList.addItem(new_item)
    
    def setupAlgos(self):
        self.addAlgo("Random")
        self.addAlgo("Random - Prefer Unexplored")
        self.addAlgo("Backtrack with memory - straight until obstructed")
        self.addAlgo("Backtracker - Shortcutter")
        self.addAlgo("Backtracker - Shortcutter - Prefer largest cut")
        self.addAlgo("Backtracker - Shortcutter w/ Metric")
        

    def loadSnakeMinigame(self):
        self.minigame = MiniGame(self)
        self.minigame.initState()
    
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Algosnake", None))
        self.start_button.setText(_translate("MainWindow", "Start", None))
        self.stop_button.setText(_translate("MainWindow", "Stop", None))
        self.clear_button.setText(_translate("MainWindow", "Clear Grid", None))
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
        
        #File menu
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.action_Open.setText(_translate("MainWindow", "&Load Grid...", None))
        self.action_Save.setText(_translate("MainWindow", "&Save Grid As...", None))
        self.action_minigame.setText(_translate("MainWindow", "S&nake Mini-Game", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))