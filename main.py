import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QShortcut, qApp, QDesktopWidget, QFileDialog, QMessageBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from functools import partial


import os
import sys
from utils import container_to_save_data



class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("test_ui.ui", self)
        self.init_UI()
    def init_UI(self) -> None:
      
        self.shortcut_exit = QShortcut(QKeySequence('ctrl+q'), self)
        self.shortcut_exit.activated.connect(qApp.quit)
        self.from_button = self.findChild(QPushButton, "from_button")
        self.to_button = self.findChild(QPushButton, "to_button")
        self.from_lable = self.findChild(QLabel, "from_lable")
        self.tmp_layout = self.findChild(QHBoxLayout, "horizontalLayout")
        self.to_label = self.findChild(QLabel, "to_lable")
        self.from_button.clicked.connect(partial(self.__input_path,self.from_lable))
        self.to_button.clicked.connect(partial(self.__input_path,self.to_label))

        self.tmp_button = self.findChild(QPushButton, "tmp_button")
        self.stats_lable = self.findChild(QLabel, "stats_lable")

        self.external = container_to_save_data("tmp", "tmp1", 0)
        self.tmp_button.clicked.connect(self.is_equal)

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
        self.timer.timeout.connect(self.counter)


        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())

        self.show()
    def start(self):
        self.timer.start()
        print(self.t)
    def counter(self):
        print("check")
        self.is_equal()
        # self.t+=1
        # self.time.setText(f"Time is {self.t}")
         

    def is_equal(self):
        self.timer.start()
        if self.external.cmp_folder(self.from_lable.text(), self.to_label.text()):
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