#!/bin/env python2.7
## Algosnake              ##
##                        ##
## algosnake.pyw          ##
##                        ##
##                        ##
## Kyle Claisse 2017      ##
############################

import sys
from algosnake_ui import *
from PyQt4 import QtGui

#This is required to override the closeEvent
class SnakeMainWindow(QtGui.QMainWindow):
    def closeEvent(self, event):
        #We first emit the closing signal, then we actually close
        self.emit(QtCore.SIGNAL("appClosing"))
        super(SnakeMainWindow, self).closeEvent(event)



def main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = SnakeMainWindow()
    ui = Algosnake_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.ui = ui
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()