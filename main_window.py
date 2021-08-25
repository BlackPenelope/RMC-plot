import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from dialog.element_view_dialog import ElementsViewDialog

from core.elements import ELEMENTS

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RMC plot")
                
        # dict {botton, row}
        self.select_button = {}
        # dict {row, combo}
        self.select_combo = {}
        
        self.init_gui()
        
    def init_gui(self):

        self.central_widget = QtWidgets.QWidget(self)

        vbox = QtWidgets.QVBoxLayout(self.central_widget)
        fig = Figure()
        canvas = FigureCanvas(fig)

        # graph axes
        canvas.axes = fig.add_subplot(111)
        canvas.axes.plot([1, 2, 3], [2, 3, 4])
        canvas.setParent(self.central_widget)
        FigureCanvas.setSizePolicy(canvas, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(canvas)

        vbox.addWidget(canvas)
        
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
        
        # open, clear button
        widget = QtWidgets.QWidget(self)        
        hbox = QtWidgets.QHBoxLayout(widget)
        
        open_button = QtWidgets.QPushButton("Open")
        open_button.clicked.connect(self.on_open)
        
        open_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(open_button)
        
        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(clear_button)
        
        elemens = []
        for ele in ELEMENTS:
            ele_str = '{0}({1}) - {2}'.format(ele.symbol, ele.number, ele.name)
            elemens.append(ele_str)            
                        
        combo = QtWidgets.QComboBox()      
        combo.addItems(elemens)
        hbox.addWidget(combo)
        
        hbox.addStretch()
                
        widget.setLayout(hbox)
        vbox.addWidget(widget)
        
        # Table
        self.table = QtWidgets.QTableWidget()   
        headers = ['elem','select']
        
        #self.table.clicked.connect(self.view_clicked)
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 150) # element column
        self.table.setColumnWidth(1, 50)
        self.table.setRowCount(3)
        self.table.setHorizontalHeaderLabels(headers)
        vbox.addWidget(self.table)
        
        for row in range(3):
            
            combo = QtWidgets.QComboBox()            
            combo.addItems(elemens)
            
            self.select_combo[row] = combo            
            
            ''' change Align
            combo.setEditable(True)
            line_edit = combo.lineEdit()
            line_edit.setAlignment(QtCore.Qt.AlignCenter)
            line_edit.setReadOnly(True)
            '''        
            i = self.table.model().index(row, 0)
            self.table.setIndexWidget(i, combo)
            
            button = QtWidgets.QPushButton('...')
            button.clicked.connect(self.select_ele)
            self.select_button[button] = row
            i = self.table.model().index(row, 1)
            self.table.setIndexWidget(i, button)
                
        # Ok button
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accepted)        
        
        vbox.addWidget(button_box)

        self.setCentralWidget(self.central_widget)
        
        self.show()
    
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

    def on_open(self):        
        pass
        