# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 13:48:54 2021

@author: Morita-T1700
"""

import os
import sys

from PyQt5 import QtCore, QtWidgets
from main_window import MainWindow

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
        
    sys.exit(app.exec_())
    
