import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from dialog.element_view_dialog import ElementsViewDialog

from core.elements import ELEMENTS
from core.results import Results
from core.rmc_configuration import RmcConfiguration
import utils.grsq

import random
import numpy as np

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RMC plot")
        self.results = Results()
                
        # dict {botton, row}
        self.select_button = {}
        # dict {row, combo}
        self.select_combo = {}
        
        self.init_gui()
        
        self.elemens = []
        for ele in ELEMENTS:
            ele_str = '{0}({1}) - {2}'.format(ele.symbol, ele.number, ele.name)
            self.elemens.append(ele_str)            

        
    def init_gui(self):

        self.central_widget = QtWidgets.QWidget(self)

        vbox = QtWidgets.QVBoxLayout(self.central_widget)
        fig = Figure()
        self.canvas = FigureCanvas(fig)

        # graph axes
        self.canvas.axes = fig.add_subplot(111)
        self.canvas.axes.plot([1, 2, 3], [2, 3, 4])
        self.canvas.setParent(self.central_widget)
        FigureCanvas.setSizePolicy(self.canvas, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self.canvas)

        vbox.addWidget(self.canvas)
        
        # element 
        widget = QtWidgets.QWidget(self)
                
        hbox = QtWidgets.QHBoxLayout(widget)
        label = QtWidgets.QLabel("Elements : ", widget)
        label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(label)
        self.elem1_combo = QtWidgets.QComboBox(widget)                
        self.elem2_combo = QtWidgets.QComboBox(widget)
        hbox.addWidget(self.elem1_combo)
        hbox.addWidget(self.elem2_combo)
        
        widget.setLayout(hbox)        
        vbox.addWidget(widget)
        
        # open, clear calc. button
        widget = QtWidgets.QWidget(self)        
        hbox = QtWidgets.QHBoxLayout(widget)
        
        open_button = QtWidgets.QPushButton("Open")
        open_button.clicked.connect(self.on_open)
        open_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(open_button)
        
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(clear_button)
                                
        calc_button = QtWidgets.QPushButton("Calc.")
        calc_button.clicked.connect(self.on_calc)
        calc_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)        
        hbox.addWidget(calc_button)
        
        hbox.addStretch()
                
        widget.setLayout(hbox)
        vbox.addWidget(widget)
        
        # Table
        self.table = QtWidgets.QTableWidget()   
        headers = ['num.', 'elem','select']
        
        #self.table.clicked.connect(self.view_clicked)
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 100) # element column
        self.table.setColumnWidth(1, 150) # element column
        self.table.setColumnWidth(2, 50)
        self.table.setHorizontalHeaderLabels(headers)
        vbox.addWidget(self.table)
                
        # Ok button
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accepted)        
        
        vbox.addWidget(button_box)

        self.setCentralWidget(self.central_widget)
        
        self.show()
        
    def update(self):
        pass
    
    def set_table(self):
        
        cfg = self.results.cfg
        #print(cfg.nmol_types)
        
        self.table.setRowCount(cfg.nmol_types)
        for row in range(cfg.nmol_types):
            
            combo = QtWidgets.QComboBox()            
            combo.addItems(self.elemens)
            
            self.select_combo[row] = combo            
            
            ''' change Align
            combo.setEditable(True)
            line_edit = combo.lineEdit()
            line_edit.setAlignment(QtCore.Qt.AlignCenter)
            line_edit.setReadOnly(True)
            '''        
            # number
            i = self.table.model().index(row, 0)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setText('{0}'.format(cfg.ni[row]))
            self.table.setItem(row, 0, item)
            
            # element
            i = self.table.model().index(row, 1)
            self.table.setIndexWidget(i, combo)
            
            # select button
            button = QtWidgets.QPushButton('...')
            button.clicked.connect(self.select_ele)
            self.select_button[button] = row
            i = self.table.model().index(row, 2)
            self.table.setIndexWidget(i, button)
        
    
    def view_clicked(self, clicked_index):
        print(clicked_index.row())
        
    def select_ele(self):
        dialog = ElementsViewDialog(self)
        result = dialog.exec()
        ele = dialog.selected
        
        button = self.sender()
        row = self.select_button[button]        
        
        combo = self.select_combo[row]        
        for i in range(combo.count()):
            if ele + '(' in combo.itemText(i):
                combo.setCurrentIndex(i)
    
    def accepted(self):
        self.close()
        
    def on_calc(self):
        '''
        l = [random.randint(0, 10) for i in range(4)]
        self.canvas.axes.cla()
        self.canvas.axes.plot([0, 1, 2, 3], l)
        
        l = [random.randint(0, 10) for i in range(4)]        
        self.canvas.axes.plot([0, 1, 2, 3], l)
        self.canvas.draw()
        '''
        
        dr = 0.05
        ntypes = self.results.cfg.nmol_types
        npar = int(ntypes*(ntypes+1)/2)
        coeff = np.zeros(npar)
        
        n = 0
        for i in range(ntypes):
            for j in range(i, ntypes):
                #ic = i*(2*ntypes-i-1)/2 + j                
                coeff[n] = 1.0
                n = n + 1

        r, gr, total_gr = utils.grsq.calc_gr(self.results.cfg, dr, coeff)
        self.results.r = r
        self.results.gr = gr
        self.results.total_gr = total_gr
        
        gr = self.results.gr.transpose()
        
        self.canvas.axes.cla()
        for i in range(npar):
            self.canvas.axes.plot(self.results.r, gr[i])
        
        #l = [random.randint(0, 10) for i in range(4)]
        #self.canvas.axes.cla()
        #self.canvas.axes.plot([0, 1, 2, 3], l)        
        self.canvas.draw()

    def on_open(self):        
        cfg_file = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                  'Select RMC file', 
                                                  './',
                                                  'All(*.*);;RMC file(.cfg)')
        
        self.results.path = cfg_file[0]
        self.results.cfg = RmcConfiguration()
        self.results.cfg.read(self.results.path)
        
        self.set_table()
        