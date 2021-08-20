import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        
        widget = QtWidgets.QWidget(self)        
        
        hbox = QtWidgets.QHBoxLayout(widget)
        
        open_button = QtWidgets.QPushButton("Open")
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
