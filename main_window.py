import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from dialog.element_view_dialog import ElementsViewDialog

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RMC plot")
        
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
        
        hbox.addStretch() 
                
        widget.setLayout(hbox)
        
        vbox.addWidget(widget)
        
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | 
                                                QtWidgets.QDialogButtonBox.Cancel)
        
        vbox.addWidget(button_box)

        self.setCentralWidget(self.central_widget)
        
        self.show()

    def on_open(self):        
        dialog = ElementsViewDialog(self)
        dialog.show()
        