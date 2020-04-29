from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QImage, QPixmap
from PyQt5.QtCore import Qt
from math import sin, cos, exp, sqrt
from horizon import float_horizon


red = Qt.red
blue = Qt.blue
black = Qt.black
white = Qt.white


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QGraphicsScene(0, 0, 711, 601)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(710, 600, QImage.Format_Alpha8)
        self.image.fill(black)
        self.pen = QPen(black)
        self.draw.clicked.connect(lambda: draw(self))
        self.dial_x.valueChanged.connect(lambda: draw(self))
        self.dial_y.valueChanged.connect(lambda: draw(self))
        self.dial_z.valueChanged.connect(lambda: draw(self))
        self.funcs.addItem("- sin(x**2 + y**2)")
        self.funcs.addItem("(sin(sqrt(x**2 + y**2)))/(sqrt(x**2 + y**2))")
        # self.funcs.addItem("exp((- x**2 - y**2) * x)")
        self.funcs.addItem("sqrt(x**2 + y**2) + 3 * (cos(sqrt(x**2 + y**2))) + 5")


def f1(x, y):
    return - sin(x**2 + y**2)

def f2(x, y):
    return (sin(sqrt(x**2 + y**2)))/(sqrt(x**2 + y**2))

def f3(x, y):
    return exp((- x**2 - y**2) * x)

def f4(x, y):
    return sqrt(x**2 + y**2) + 3 * (cos(sqrt(x**2 + y**2))) #+ 5 
    # без комментария тоже работает, но выпадает за границы обзора



def draw(win):
    win.scene.clear()
    win.image.fill(black)
    tx = win.dial_x.value()
    ty = win.dial_y.value()
    tz = win.dial_z.value()

    if win.funcs.currentText() == "- sin(x**2 + y**2)":
        f = f1

    if win.funcs.currentText() == "(sin(sqrt(x**2 + y**2)))/(sqrt(x**2 + y**2))":
        f = f2

    if win.funcs.currentText() == "exp((- x**2 - y**2) * x)":
        f = f3

    if win.funcs.currentText() == "sqrt(x**2 + y**2) + 3 * (cos(sqrt(x**2 + y**2))) + 5":
        f = f4

    win.image = float_horizon(win.scene.width(), win.scene.height(), win.x_min.value(), win.x_max.value(), win.dx.value(),
            win.z_min.value(), win.z_max.value(), win.dz.value(), tx, ty, tz, f, win.image)

    pix = QPixmap()
    pix.convertFromImage(win.image)
    win.scene.addPixmap(pix)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())