import sys

try:
    import PyQt6
    print("PyQt6 is installed")
except ImportError:
    print("PyQt6 is not installed")
    print("Install PyQt6 by running:")
    print("pip install PyQt6")
    print("Exiting...")
    exit(1)

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QColorDialog
from PyQt6.QtGui import QPainter, QColor, QMouseEvent, QPen, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer

SIZES = ["1", "2", "3", "4", "5", "6","8", "10", "12", "16", "20", "30", "50"]

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MUpainter")
        self.setFixedSize(QSize(1280,780))

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)

        mainlayout = QHBoxLayout(central_widget)

        self.wks = Workspace() 
        mainlayout.addWidget(self.wks, stretch=4) #stretch=4

        self.mu = MUcolorwheel(self.wks)
        self.szt = setSizeToggle(self.wks) 
        mainlayout.addWidget(self.mu, stretch=1)
        mainlayout.addWidget(self.szt, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // 60)


class Workspace(QWidget):    
    def __init__(self):
        super().__init__()

        self.canvas = QPixmap(800,800)
        self.canvas.fill(Qt.GlobalColor.white)

        self.drawing = bool(False)
        self.points = []

        self.pen_color = QColor(0,0,0)
        self.pen_width = 4

    def set_pen_color(self,color):
        self.pen_color = color

    def set_pen_width(self,width):
        self.pen_width = width

    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = bool(True) #if the mouse left button is clicked, the "drawing" is true
            self.points.append(event.position()) 
            self.update()
                
    def mouseReleaseEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = bool(False)
            self.points = []

    def mouseMoveEvent(self, event:QMouseEvent):
        if self.drawing : 
            self.points.append(event.position())
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self.canvas)
        pen = QPen(self.pen_color)
        pen.setWidth(self.pen_width)
        painter.setPen(pen)

        if self.points:
            for i in range(len(self.points) - 1): 
                point1 = self.points[i]
                point2 = self.points[i + 1]
                painter.drawLine(point1, point2)

        widget_painter = QPainter(self)
        widget_painter.drawPixmap(0, 0, self.canvas)

class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(10,10))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class setSizeToggle(QWidget):
    def __init__(self,workspace):
        super().__init__()

        self.workspace = workspace
        self.sizes = QVBoxLayout()
        self.add_pensize_toggle(self.sizes)
        self.l = QVBoxLayout()
        self.l.addLayout(self.sizes)
        self.setLayout(self.l)

    def add_pensize_toggle(self, layout):
        for s in SIZES:
            b = QSizeButton(s)
            b.pressed.connect(lambda s=s: self.workspace.set_pen_width(int(s)))
            layout.addWidget(b)       

class QSizeButton(QPushButton):
    def __init__(self, size):
        super().__init__()
        self.setText(str(size)) 
        self.setFixedSize(QSize(20, 20)) 
        
        self.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 12px;
                border: 2px solid white;
                box-shadow: 0px 0px 0px 2px #fff;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """)

class MUcolorwheel(QWidget):
    def __init__(self, workspace):
        super().__init__()
        self.workspace = workspace

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.color_button = QPushButton("Pick a color")
        self.color_button.setStyleSheet("color: white; background-color: black;)")
        self.color_button.clicked.connect(self.colorpicker)
        layout.addWidget(self.color_button)

    def colorpicker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.workspace.set_pen_color(color)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

try: 
    sys.exit(app.exec())
except:
    print("the system was completely shut down")
