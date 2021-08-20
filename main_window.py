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

        self.setCentralWidget(self.central_widget)
        
        self.show()
