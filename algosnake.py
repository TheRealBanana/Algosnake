#!/bin/env python2.7
## Algosnake              ##
##                        ##
## algosnake.pyw          ##
##                        ##
## revision: 002          ##
##                        ##
## Kyle Claisse 2017      ##
############################

import sys
import re
from algosnake_ui import *
from PyQt4 import QtGui

def main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Algosnake_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.ui = ui
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()