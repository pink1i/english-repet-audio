import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QRectF
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsGridLayout, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("My App")
    layout = QVBoxLayout()
    scene = QGraphicsScene()
    self.rec1 = QRectF(-10, -10, 50, 50)
    scene.addRect(self.rec1)
    view =  QGraphicsView(scene)
    view.setMouseTracking(True)
    layout.addWidget(view)
    widget = QWidget()
    widget.setLayout(layout)
    self.setCentralWidget(widget)

  def mousePressEvent(self, e):
    print(e.pos())
    print(self.rec1.x())

  def mouseMoveEvent(self.view, e):
    # self.rec1.setX(e.)
    print(e.pos())

app = QApplication(sys.argv)

windown = MainWindow()
windown.show()

app.exec_()
