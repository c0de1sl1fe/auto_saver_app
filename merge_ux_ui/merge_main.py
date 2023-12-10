import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5.QtGui import QMovie, QIcon

from sidebar import Ui_MainWindow

import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QShortcut, qApp, QMenu, QAction, QInputDialog,QLineEdit, QDesktopWidget, QDialog, QFileDialog, QMessageBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTimeEdit, QRadioButton, QCheckBox, QStatusBar, QSystemTrayIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from functools import partial

import time

import os
import sys
from utils import container_to_save_data









class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)



        self.init_UI()


    # Function for searching
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        search_text = self.ui.search_input.text().strip()
        if search_text == "Home" or search_text == "home":
            self.ui.stackedWidget.setCurrentIndex(0)
            return
        if search_text == "dashboard" or search_text == "Dashboard":
            self.ui.stackedWidget.setCurrentIndex(1)
            return
        if search_text == "user page" or search_text == "user":
            self.ui.stackedWidget.setCurrentIndex(2)
            return
        
        if search_text:
            self.movie = QMovie("img/2loading_gif.gif")
            self.ui.photo_lable.setMovie(self.movie)
            self.movie.start()
            self.ui.label_6.setText(f"The page \"{search_text}\" doesn't exist")

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        print("on user")
        self.ui.stackedWidget.setCurrentIndex(2)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        print(btn_list)
        
        for btn in btn_list:
            print(btn.text(), index)
            if index in [3, 3]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashboard_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_dashboard_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def init_UI(self) -> None:

        # tray 
        self.tray_icon = QSystemTrayIcon(QIcon("add/icon/logo.png"))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


        self.dst = ""
        self.src = ""
        self.dst_list = []
        self.shortcut_exit = QShortcut(QKeySequence('ctrl+q'), self)
        self.shortcut_exit.activated.connect(qApp.quit)
 
        self.ui.from_button.clicked.connect(
            partial(self.__input_path, self.ui.from_lable))
        self.ui.to_button.clicked.connect(
            partial(self.__input_path, self.ui.to_lable))

        self.ui.time_holder = self.findChild(QTimeEdit, "time_holder")
        self.ui.time_holder.setDisplayFormat("m (n)")
        # self.time_holder.editingFinished.connect(self.update_time)
        self.time_for_timer = 0
        self.ui.time_button.clicked.connect(self.update_time)

        self.check_boxes = []
        self.check_boxes.append(self.ui.Check_box_1)
        self.check_boxes.append(self.ui.Check_box_2)
        self.check_boxes.append(self.ui.Check_box_3)



        self.external = container_to_save_data("tmp", "tmp1", 0)
        # self.tmp_button.clicked.connect(self.is_equal)
        self.ui.tmp_button.clicked.connect(self.setup_backup)

        # self.setWindowTitle("test")
        # self.resize(400, 400)

        self.ui.recovery_button.clicked.connect(self.recover)
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
            print(f"backup {self.external.full_backup(self.src, self.dst_list[-1], self.ignore_pattern)}")  
            
        if not self.external.cmp_folder(self.src, self.dst_list[-1], self.ignore_pattern):
            self.dst_list.append(self.external.create_name(self.src, self.dst))
            print(f"backup {self.external.full_backup(self.src, self.dst_list[-1], self.ignore_pattern)}")    
        else:
            print("equal")
            self.ui.stats_lable.setText(f"last backup: {os.path.basename(self.dst_list[-1])}")
        print("_timer_end_")

    def update_time(self):
        value = self.ui.time_holder.time().toPyTime()
        print(f"{value.hour} {value.minute}")
        self.time_for_timer = value.minute*60*60  # tmp

    def recover(self):
        # self.status_bar.showMessage(f"Checkbox is {self.check_box_1.isChecked()}")
        # self.status_bar.showMessage(f"Checkbox {self.check_boxes[0].text()} is {self.check_boxes[0].isChecked()}")
        if self.dst_list:
            text, ok = QInputDialog.getItem(self, 'Choose what to recover', 'List:', self.dst_list)
            if ok and text:
                print(text)
        else:
            QMessageBox.about(self, "No recover option", "There's nothing to recover")



    # test close event
    def closeEvent(self, event):
        check_box = None
        # if self.ui.Check_box_1.isChecked():
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def setup_backup(self):
        if self.timer.isActive():
            self.timer.stop()
            print(f"timer is {self.timer.isActive()}")
            self.ui.tmp_button.setText("Start")
        else:
            self.ignore_pattern.clear()
            for i in self.check_boxes:
                if i.isChecked():
                    self.ignore_pattern.append(i.text())
            print(self.time_for_timer)
            print(self.time_for_timer, self.ui.to_lable.text(), self.ui.from_lable.text() )
            if self.time_for_timer > 0 and self.ui.to_lable.text() != "to" and self.ui.to_lable.text() and self.ui.from_lable.text() != "to" and self.ui.from_lable.text():
                self.timer.setInterval(self.time_for_timer)
                self.src = self.ui.from_lable.text()
                self.dst = self.ui.to_lable.text()
                self.timer.start()
                print(
                    f"timer is {self.timer.isActive()}")
                print(f"time {self.time_for_timer} src {self.src} dst {self.dst}")
                self.ui.tmp_button.setText("Stop")
            else:
                print('sad')
                print(
                    f"timer is {self.timer.isActive()} and it's because: {self.time_for_timer} or src {self.src} or dst {self.dst}")
            # self.status_bar.showMessage(f"timer is {self.timer.isActive()}")
            print(self.ignore_pattern)
            # print(f"timer is {self.timer.isActive()}")

    def is_equal(self):
        self.timer.start()
        if self.external.cmp_folder(self.from_label.text(), self.to_label.text()):
            self.ui.stats_lable.setText("True")
            self.ui.stats_lable.setStyleSheet("border: 3px solid green;")
        else:
            self.ui.stats_lable.setText("false")
            self.ui.stats_lable.setStyleSheet("border: 3px solid red;")

    def __input_path(self, label: QLabel) -> None:
        """service function"""
        tmp = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if not tmp:
            QMessageBox.critical(
                self, "Error", "please select dir", QMessageBox.Ok)
        else:
            label.setText(tmp)
            # print into status_bar





if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ## loading style file
    # with open("add/style.qss", "r") as style_file:
    #     style_str = style_file.read()
    # app.setStyleSheet(style_str)

    ## loading style file, Example 2

    style_file = QFile("add/style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())
    
    

    
    window = MainWindow()
    window.show()
    


    sys.exit(app.exec())

