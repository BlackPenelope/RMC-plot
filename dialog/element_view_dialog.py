# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 17:16:17 2021

@author: Morita-T1700
"""

from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, 
                            QGridLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from core.elements import ELEMENTS, SERIES

import platform

COLORS = {
    1: (0x99, 0xff, 0x99),  # Nonmetals
    2: (0xc0, 0xff, 0xff),  # Noble gases
    3: (0xff, 0x99, 0x99),  # Alkali metals
    4: (0xff, 0xde, 0xad),  # Alkaline earth metals
    5: (0xcc, 0xcc, 0x99),  # Metalloids
    6: (0xff, 0xff, 0x99),  # Halogens
    7: (0xcc, 0xcc, 0xcc),  # Poor metals
    8: (0xff, 0xc0, 0xc0),  # Transition metals
    9: (0xff, 0xbf, 0xff),  # Lanthanides
    10: (0xff, 0x99, 0xcc),  # Actinides
}


SPACER = 12
if platform.system() == 'Windows':
    SPACER = 28
elif platform.system() == 'Darwin':
    SPACER = 12
elif platform.system() == 'Linux':
    SPACER = 28

class ElementsViewDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        
        self.setWindowTitle('Elements View')
        
        self.layout = """
        .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  18 .
        1  H  2  .  .  .  .  .  .  .  .  .  .  13 14 15 16 17 He .
        2  Li Be .  .  .  .  .  .  .  .  .  .  B  C  N  O  F  Ne .
        3  Na Mg 3  4  5  6  7  8  9  10 11 12 Al Si P  S  Cl Ar .
        4  K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr .
        5  Rb Sr Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I  Xe .
        6  Cs Ba *  Hf Ta W  Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn .
        7  Fr Ra ** Rf Db Sg Bh Hs Mt .  .  .  .  .  .  .  .  .  .
        .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
        .  .  .  *  La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu .
        .  .  .  ** Ac Th Pa U  Np Pu Am Cm Bk Cf Es Fm Md No Lr .
        """
        
        rows = len(self.layout.splitlines()) - 2
        cols = len(self.layout.splitlines()[1].split())
                
        self.grid = QGridLayout()
        #self.grid.setRowStretch(6, 4)
        self.grid.setSpacing(2)        
        self.buttons = list(range(0, len(ELEMENTS)))
        self.selected_button = None
        self.selected = ''
        self.elem_button = {}
                
        button_size = 30
        
        nrow = 0
        for row in self.layout.splitlines()[1:-1]:            
            self.grid.setRowMinimumHeight(nrow, button_size + 1)
            ncol = 0
            for col in row.split():
                
                if nrow == 0:
                    self.grid.setColumnMinimumWidth(ncol, button_size + 1)
                
                if col == '.':               
                    label = QtWidgets.QLabel('', self)
                    label.setFixedSize(SPACER, SPACER)
                    self.grid.addWidget(label, nrow, ncol)                    
                    pass
                    #self.sizer.Add((SPACER, SPACER))
                elif col[0] in '123456789*':
                    static = QtWidgets.QLabel(col,self)
                    #static.setFixedSize(SPACER, SPACER)
                    static.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
                    static.setStyleSheet('font-weight: bold;')
                    self.grid.addWidget(static, nrow, ncol)
                else:
                    ele = ELEMENTS[col]
                    button = QPushButton(ele.symbol, self)
                    button.setCheckable(True) # Toggle
                    button.toggled.connect(self.button_toggled)                    
                    self.elem_button[ele.symbol] = button
                    col = COLORS[ele.series]                    
                    style = 'background-color: rgb({0}, {1}, {2}); font-weight: bold;'.format(col[0], col[1], col[2])
                    button.setStyleSheet(style)
                    #button.setStyleSheet('QPushButton {background-color: rgb(255,0,0); color: red;}')
                    #button.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                    button.setFixedSize(QSize(button_size, button_size))                    
                    self.grid.addWidget(button, nrow, ncol)
                
                ncol = ncol + 1
            nrow = nrow + 1
            
        vbox = QVBoxLayout()
        vbox.addLayout(self.grid)
        
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | 
                                                QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.okButtonClicked)
        button_box.rejected.connect(self.cancelButtonClicked)
        
        vbox.addWidget(button_box)
        
        self.setLayout(vbox)
    
    def button_toggled(self, checked):
        source = self.sender()
        symbol = source.text()
        
        if not self.selected_button is None:
            self.selected_button.setChecked(False)
        
        self.selected_button = self.elem_button[symbol]
        self.selected = symbol
        
    def okButtonClicked(self):        
        self.close()

    def cancelButtonClicked(self):
        self.close()
        