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
DEFAULT_VOLUME = 20

def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 3600000
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return f"{h}:{m}:{s}" if h else f"{m}:{s}"

def hhmmssmm(ms):
    if ms < 0: return "0"
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


def ms_to_Qtime(ms):
  h, r = divmod(ms, 3600000)
  m, r = divmod(r, 60000)
  s, mm = divmod(r, 1000)
  return QTime(h, m, s, mm)

def qtime_2_ms(v):
    m = v.minute()
    s = v.second()
    ms = v.msec()

    return m * 60000 + 1000*s + ms

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
    self.btn_play_loop.pressed.connect(self.play_section)
    self.s_volume.valueChanged.connect(self.player.setVolume)
    self.s_track_time.valueChanged.connect(self.player.setPosition)
    self.tb_subs.clicked.connect(self.on_click_row)

    self.btn_add_part.pressed.connect(self.add_sub)
    self.btn_break_start.pressed.connect(self.get_start)
    self.btn_break_end.pressed.connect(self.get_end)
    self.actionOpen.triggered.connect(self.open_file_action)
    self.actionExit.triggered.connect(self.exit_action)
    self.te_start.timeChanged.connect(self.changed_start_break)
    self.te_end.timeChanged.connect(self.changed_end_break)

    self.player.setVolume(DEFAULT_VOLUME)
    self.s_volume.setValue(DEFAULT_VOLUME)

    self.is_play_section = False
    self.start_break = 0
    self.end_break = 0

  def exit_action(self):
    sys.exit()

  def on_click_row(self, row_index_obj):
    model = self.tb_subs.model()
    for i in range(4):
      index = model.index(row_index_obj.row(), i)
      print(model.data(index))

  def open_file_action(self):
    filename, _ = QFileDialog.getOpenFileName(self, "Mo file", "/home/hong/Music/", "")
    url = QUrl.fromLocalFile(filename)
    self.content = QMediaContent(url)
    self.player.setMedia(self.content)
    print(f"Filename opened is {filename}")
    print(f"aaaaaa {self.player.duration()}")
    self.play_audio()

  def play_audio(self):
      self.player.play()
      self.is_play_section = False

  def pause_audio(self):
    self.player.pause()

  def stop_audio(self):
    self.player.stop()

  def update_position(self, position):
    print("p!", position)
    if position >= 0:
      self.lb_current_time.setText(hhmmss(position))
      if self.is_play_section and position > self.end_break:
        if self.player.state() != 1: self.player.play()
        self.player.setPosition(self.start_break)


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
    pos = self.player.position()
    self.start_break = pos
    print(f"---Start----> {hhmmssmm(pos)}")
    # print(self.te_start.time().msec())
    # print(self.te_start.time().second())
    self.te_start.setTime(ms_to_Qtime(pos))

  def get_end(self):
    pos = self.player.position()
    self.end_break = pos
    print(f"---End----> {hhmmssmm(pos)}")
    self.te_end.setTime(ms_to_Qtime(pos))

  def add_sub(self):
      rowCount = self.tb_subs.rowCount()
      print(f"Insert row {rowCount}")
      self.tb_subs.insertRow(rowCount)
      for idx, key in enumerate(self.tb_subs.headers.keys()):
          if idx == 0: item = QTableWidgetItem(str(rowCount))
          if idx == 1: item = QTableWidgetItem(self.textEdit.toPlainText())
          if idx == 2: item = QTableWidgetItem(hhmmssmm(self.start_break))
          if idx == 3: item = QTableWidgetItem(hhmmssmm(self.end_break))
          if idx == 4: item = QTableWidgetItem(hhmmssmm(self.end_break-self.start_break))
          item.setFlags(Qt.ItemIsEnabled)
          self.tb_subs.setItem(rowCount, idx, item)
      self.textEdit.clear()

  def play_section(self):
    self.is_play_section = True
    self.player.setPosition(self.start_break)
    if self.player.state() != 1: self.player.play()

  def remove_sub(self):
    pass

  def changed_start_break(self, v):
    self.start_break = qtime_2_ms(v)

  def changed_end_break(self, v):
    self.end_break = qtime_2_ms(v)


app = QApplication(sys.argv)

windown = MainWindow()
windown.show()

app.exec_()
