import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QShortcut, qApp, QDesktopWidget, QFileDialog, QMessageBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTimeEdit, QRadioButton, QCheckBox, QStatusBar
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from functools import partial

import time

import os
import sys
from utils import container_to_save_data


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("test_ui.ui", self)
        self.init_UI()

    def init_UI(self) -> None:

        self.dst = ""
        self.src = ""
        self.dst_list = []
        self.shortcut_exit = QShortcut(QKeySequence('ctrl+q'), self)
        self.shortcut_exit.activated.connect(qApp.quit)
        self.from_button = self.findChild(QPushButton, "from_button")
        self.to_button = self.findChild(QPushButton, "to_button")
        self.from_label = self.findChild(QLabel, "from_lable")
        self.tmp_layout = self.findChild(QHBoxLayout, "horizontalLayout")
        self.to_label = self.findChild(QLabel, "to_lable")
        self.from_button.clicked.connect(
            partial(self.__input_path, self.from_label))
        self.to_button.clicked.connect(
            partial(self.__input_path, self.to_label))

        self.time_holder = self.findChild(QTimeEdit, "time_holder")
        # self.time_holder.editingFinished.connect(self.update_time)
        self.time_for_timer = 0
        self.time_button = self.findChild(QPushButton, "time_button")
        self.time_button.clicked.connect(self.update_time)

        self.check_boxes = []
        self.check_boxes.append(self.findChild(QCheckBox, "Check_box_1"))
        self.check_boxes.append(self.findChild(QCheckBox, "Check_box_2"))
        self.check_boxes.append(self.findChild(QCheckBox, "Check_box_3"))
        # self.check_box_1 = self.findChild(QCheckBox, "Check_box_1")
        # self.check_box_2 = self.findChild(QCheckBox, "Check_box_2")
        # self.check_box_3 = self.findChild(QCheckBox, "Check_box_3")

        # self.check_box_1.toggled.connect(self.onClicked)
        self.check_boxes[0].toggled.connect(self.onClicked)

        self.backup_option_1 = self.findChild(QRadioButton, "backup_option_1")
        self.backup_option_2 = self.findChild(QRadioButton, "backup_option_2")
        self.backup_option_3 = self.findChild(QRadioButton, "backup_option_3")
        self.backup_option_4 = self.findChild(QRadioButton, "backup_option_4")

        self.tmp_button = self.findChild(QPushButton, "tmp_button")
        self.stats_lable = self.findChild(QLabel, "stats_lable")

        self.external = container_to_save_data("tmp", "tmp1", 0)
        # self.tmp_button.clicked.connect(self.is_equal)
        self.tmp_button.clicked.connect(self.setup_backup)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("test", 300)
        # self.setWindowTitle("test")
        # self.resize(400, 400)

        # self.t = 0
        # self.time = QLabel()

        # self.time.setText(f"Time is {self.t}")
        # self.starter = QPushButton("starter")
        # self.starter.clicked.connect(self.start)
        # self.tmp_layout.addWidget(self.time)
        # self.tmp_layout.addWidget(self.starter)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.backup)

        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())

        self.ignore_pattern = []

        self.show()

    def start(self):
        self.timer.start()
        print(self.t)

    def backup(self):
        # add backup option
        if not self.dst_list:
            self.dst_list.append(self.external.create_name(self.src, self.dst))
        if not self.external.cmp_folder(self.src, self.dst_list[-1]):
            self.external.full_backup(self.src, self.dst_list[-1], self.ignore_pattern)       
        #
        print("_timer_end_")

    def update_time(self):
        value = self.time_holder.time().toPyTime()
        self.status_bar.showMessage(f"{value.hour} {value.minute}")
        self.time_for_timer = value.minute*60*60  # tmp

    def onClicked(self):
        # self.status_bar.showMessage(f"Checkbox is {self.check_box_1.isChecked()}")
        self.status_bar.showMessage(f"Checkbox {self.check_boxes[0].text()} is {self.check_boxes[0].isChecked()}")

    def setup_backup(self):
        if self.timer.isActive():
            self.timer.stop()
            self.status_bar.showMessage(f"timer is {self.timer.isActive()}")
            self.tmp_button.setText("Start")
        else:
            self.ignore_pattern.clear()
            for i in self.check_boxes:
                if i.isChecked():
                    self.ignore_pattern.append(i.text())
            print(self.time_for_timer)

            if self.time_for_timer > 0 and self.to_label.text() != "to" and self.to_label.text() and self.from_label.text() != "to" and self.from_label.text() and (self.to_label.text() in self.from_label.text()):
                self.timer.setInterval(self.time_for_timer)
                self.src = self.from_label.text()
                self.dst = self.to_label.text()
                self.timer.start()
                self.status_bar.showMessage(
                    f"timer is {self.timer.isActive()}")
                print(f"time {self.time_for_timer} src {self.src} dst {self.dst}")
                self.tmp_button.setText("Stop")
            else:
                print('sad')
                self.status_bar.showMessage(
                    f"timer is {self.timer.isActive()} and it's because: {self.time_for_timer} or src {self.src} or dst {self.dst}")
            # self.status_bar.showMessage(f"timer is {self.timer.isActive()}")
            print(self.ignore_pattern)
            # print(f"timer is {self.timer.isActive()}")

    def is_equal(self):
        self.timer.start()
        if self.external.cmp_folder(self.from_label.text(), self.to_label.text()):
            self.stats_lable.setText("True")
            self.stats_lable.setStyleSheet("border: 3px solid green;")
        else:
            self.stats_lable.setText("false")
            self.stats_lable.setStyleSheet("border: 3px solid red;")

    def __input_path(self, label: QLabel) -> None:
        """service function"""
        tmp = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if not tmp:
            QMessageBox.critical(
                self, "Error", "please select dir", QMessageBox.Ok)
        else:
            label.setText(tmp)
            print()
            # print into status_bar


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
