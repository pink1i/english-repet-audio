import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QAbstractListModel, QTime, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsGridLayout, QTableWidgetItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from ui.wave import Ui_MainWindow
from table_widget import TableWidget
TABLE_HEADER = {
  'idx'          :'#',
  'script'       :'Script',
  'start'        :'Start Time',
  'time'         :'End Time',
  'duration'     :'Duration'
}
DEFAULT_VOLUME = 5

def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 3600000
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return f"{h}:{m}:{s}" if h else f"{m}:{s}"

def hhmmssmm(ms):
    # s = 1000
    # m = 60000
    # h = 3600000
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, mm = divmod(r, 1000)
    return f"{h}:{m}:{s}" if h else f"{m}:{s}:{mm}"

class SubsModel(QAbstractListModel):
  def __init__(self, subs=None):
    super().__init__()
    self.subs = subs or []

  def data(self, index, role):
      if role == QtCore.Qt.DisplayRole:
          sub = self.subs[index.row()]
          return sub

  def rowCount(self, index):
      return len(self.subs)




class MainWindow(QMainWindow, Ui_MainWindow):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.player = QMediaPlayer()

    self.player.positionChanged.connect(self.update_position)
    self.player.durationChanged.connect(self.update_duration)

    self.btn_play.pressed.connect(self.play_audio)
    self.btn_pause.pressed.connect(self.pause_audio)
    self.btn_stop.pressed.connect(self.stop_audio)
    self.s_volume.valueChanged.connect(self.player.setVolume)
    self.s_track_time.valueChanged.connect(self.player.setPosition)

    self.btn_break_start.pressed.connect(self.get_start)
    self.btn_break_end.pressed.connect(self.get_end)
    self.actionOpen.triggered.connect(self.open_file_action)
    self.actionExit.triggered.connect(self.exit_action)

    self.player.setVolume(DEFAULT_VOLUME)
    self.s_volume.setValue(DEFAULT_VOLUME)

  def exit_action(self):
    sys.exit()

  def open_file_action(self):
    filename, _ = QFileDialog.getOpenFileName(self, "Mo file", "/home/hong/Music/", "")
    url = QUrl.fromLocalFile(filename)
    self.content = QMediaContent(url)
    self.player.setMedia(self.content)
    print(f"Filename opened is {filename}")
    print(f"aaaaaa {self.player.duration()}")
    self.play_audio()

  def play_audio(self):
      rowCount = self.tb_subs.rowCount()
      print(f"Insert row {rowCount}")
      self.tb_subs.insertRow(rowCount)
      for idx, key in enumerate(self.tb_subs.headers.keys()):
          item = QTableWidgetItem(str(1))
          if idx != 1: item.setFlags(Qt.ItemIsEnabled)
          self.tb_subs.setItem(rowCount, idx, item)
      # self.player.play()

  def pause_audio(self):
    self.player.pause()

  def stop_audio(self):
    self.player.stop()

  def update_position(self, position):
    print("p!", position)
    if position >= 0:
      self.lb_current_time.setText(hhmmss(position))

    self.s_track_time.blockSignals(True)
    self.s_track_time.setValue(position)
    self.s_track_time.blockSignals(False)

  def on_click_track_time(self, position):
    print(f"------ {position}")

  def update_duration(self, duration):
    print("d!", duration)
    # self.player.stop()
    self.s_track_time.setMaximum(duration)
    if duration >= 0:
      self.lb_total_time.setText(hhmmss(duration))

  def get_start(self):
    print(f"---Start----> {hhmmssmm(self.player.position())}")
    print(self.te_start.time().msec())
    print(self.te_start.time().second())

  def get_end(self):
    print(f"---End----> {hhmmssmm(self.player.position())}")
    self.te_start.setTime(QTime(0,3,24,321))

app = QApplication(sys.argv)

windown = MainWindow()
windown.show()

app.exec_()
