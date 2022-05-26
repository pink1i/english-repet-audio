from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, \
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
TABLE_HEADER = {
  'idx'          :'#',
  'script'       :'Script',
  'start'        :'Start Time',
  'time'         :'End Time',
  'duration'     :'Duration'
}

TABLE_HEADER_WIDTH = [5, 420, 100, 100, 100]

class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.headers = kwargs.get('v_headers', TABLE_HEADER)
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers.values())
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._data = None
        for idx, col_width in enumerate(TABLE_HEADER_WIDTH):
          self.setColumnWidth(idx, col_width)


    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, value):
        self._data = value
        if isinstance(self._data, list):
            for i in self._data:
                i.attach(self)

        self._render()


    def _render(self):
        print('render')
        rowCount = self.rowCount()
        # clear old value
        if rowCount != 0:
            for i in range(rowCount-1, -1, -1):
                self.removeRow(i)
                print(f"Remove row {i}")

        for i in range(len(self.data)):
            print(f"Inserted row {i}")
            self.insertRow(i)
            for idx, key in enumerate(self.headers.keys()):
                self.setItem(i, idx, QTableWidgetItem(str(getattr(self.data[i], key))))

    def update(self):
        print('update')
        self._render()


    def contextMenuEvent(self, event):
        runAction = QAction('Run', self)
        exitAction = QAction('Exit', self)
        self.menu = QMenu(self)
        copy_action = self.menu.addAction(runAction)
        copy_action = self.menu.addAction(exitAction)
        action = self.menu.exec_(self.mapToGlobal(event.pos()))
        runAction.triggered.connect(lambda _: self.run())
        runAction.triggered.connect(lambda _: self.on_exit())
        # print(action)
        gp = event.globalPos()
        vp = self.viewport().mapFromGlobal(gp)

        if action == runAction:
            # print((self.rowAt(vp.y()), self.columnAt(vp.x())))
            self.run(self.rowAt(vp.y()))
        # renameAction.triggered.connect(lambda: self.renameSlot(event))
        # self.menu.addAction(renameAction)
        # # add other required actions
        # self.menu.popup(QtGui.QCursor.pos())


    def run(self, index):
        print(f"Pass data[{index}]")
        self.parent_windows.run_job(index)


    def _update(self, rowCount, sc):
        self.setItem(rowCount, 0, QTableWidgetItem("0"))
        self.setItem(rowCount, 1, QTableWidgetItem(str(sc.job_type)))
        self.setItem(rowCount, 2, QTableWidgetItem(str(sc.current_time)))
        self.setItem(rowCount, 3, QTableWidgetItem(str(sc.time)))
        self.setItem(rowCount, 4, QTableWidgetItem(str(sc.status)))
        self.setItem(rowCount, 5, QTableWidgetItem(str(sc.duration)))
        self.setItem(rowCount, 6, QTableWidgetItem(str(sc.started_at)))
        self.setItem(rowCount, 7, QTableWidgetItem(str(sc.ended_at)))


    def on_exit(self):
        print("on_exit")
