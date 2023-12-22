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
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QShortcut, qApp, QMenu, QAction, QInputDialog, QLineEdit, QDesktopWidget, QDialog, QFileDialog, QMessageBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QTimeEdit, QRadioButton, QCheckBox, QStatusBar, QSystemTrayIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from functools import partial

import time

import os
import sys

from utils import InterfaceFileOperation


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.recovery_button.setVisible(False)
        self.ui.stackedWidget.setCurrentIndex(2)
        # for i in range(0, 2):
        #     self.ui.stackedWidget.widget(i).setVisible(False)

        self.ui.search_btn.setVisible(False)
        # test = self.ui.stackedWidget.widget(0)
        # print(test.setVisible(False))
        # self.ui.home_btn_2.setChecked(True)

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
            self.movie = QMovie("icon/2loading_gif.gif")
            self.ui.photo_lable.setMovie(self.movie)
            self.movie.start()
            self.ui.label_6.setText(
                f"The page \"{search_text}\" doesn't exist")

    # Function for changing page to user page
    def on_user_btn_clicked(self):
        print("on user")
        self.ui.stackedWidget.setCurrentIndex(2)

    # Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
            + self.ui.full_menu_widget.findChildren(QPushButton)
        for btn in btn_list:
            if index in [3, 3]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)


    # functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget.widget(0).setVisible(self.check)

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget.widget(0).setVisible(self.check)

    def on_dashboard_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget.widget(1).setVisible(self.check)

    def on_dashboard_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget.widget(1).setVisible(self.check)

    def login(self):
        login = self.ui.login_line.text()
        pas = self.ui.password_line.text()
        # if True:
        
        if self.external.check_user(login, pas):
        # if True:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.check = True
            self.ui.search_btn.setVisible(True)
            self.ui.login_button.setVisible(False)
        else:
            QMessageBox.warning(
                    self, "Warning", f"Wrong login or password", QMessageBox.Ok)
            if self.count_login>4:
                QMessageBox.critical(
                    self, "Fatal error", f"You gone beyond the limit number of entrance, \nprogram end", QMessageBox.Ok)
                print(self.count_login)
                qApp.quit()
            self.count_login+=1


    def init_UI(self) -> None:
        # tray
        self.tray_icon = QSystemTrayIcon(QIcon("icon/Logo.png"))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        self.backup_action = QAction("backup", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        self.backup_action.triggered.connect(self.setup_backup)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        tray_menu.addAction(self.backup_action)
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

        # self.ui.time_holder = self.findChild(QTimeEdit, "time_holder")
        self.ui.time_holder = self.findChild(QSpinBox, "timer_holder")
        self.ui.timer_holder.setSuffix(" min")
        # self.ui.time_holder.setDisplayFormat("m (n)")
        self.ui.time_holder.setRange(0, 10)
        self.ui.timer_holder.setValue(0)

        self.time_for_timer = 0
        self.ui.time_button.clicked.connect(self.update_time)

        self.check_boxes = []

        self.check_boxes = self.ui.stackedWidget.findChildren(QCheckBox)

        self.external = InterfaceFileOperation()
        self.ui.tmp_button.clicked.connect(self.setup_backup)

        self.setWindowTitle("AutoSaver")
        self.setWindowIcon(QIcon("icon/logo.png"))

        self.ui.recovery_button.clicked.connect(self.setup_recover)

        self.count_fancy_backup = 0
        self.repeat = 2

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.ignore_pattern = []

        self.check = False
        self.ui.password_line.setEchoMode(QLineEdit.Password)
        self.ui.login_button.clicked.connect(self.login)

        a = QMessageBox.about(self, "Loading...",
                    "Please wait, loading data")
        self.external.load_login()
        self.count_login = 0
        self.show()

    def __clean_array(self):
        for i in self.dst_list:
            if not os.path.exists(i):
                self.dst_list.remove(i)

    def __zip_array(self):
        if len(self.dst_list) >= 2:
            for i in range(len(self.dst_list)-1):
                self.dst_list[i] = self.external.ziping(self.dst_list[i])

    def __backup__(self):
        if not self.external.full_backup(self.src, self.dst_list[-1], self.ignore_pattern):
            QMessageBox.warning(
                self, "Warning", f"Something went wrong: \nbackup failed", QMessageBox.Ok)
            if self.timer.isActive():
                self.timer.stop()
            self.dst_list.remove(self.dst_list[-1])
            return False
        return True

    def backup(self):
        # add backup option
        if not self.external.is_dir(self.src):
            QMessageBox.warning(
                self, "Warning", f"Something went wrong: \nsrc - {self.src} doesnt't exist", QMessageBox.Ok)
            if self.timer.isActive():
                self.timer.stop()
            return

        if not self.dst_list and self.external.is_dir(self.src):
            self.dst_list.append(self.external.create_name(self.src, self.dst))
            self.__backup__()
            self.ui.stats_lable.setText(
                f"last backup: {os.path.basename(os.path.split(self.dst_list[-1])[0])}")
            return

        if not self.external.cmp_folder(self.src, self.dst_list[-1], self.ignore_pattern):
            self.dst_list.append(self.external.create_name(self.src, self.dst))
            self.__backup__()
            self.ui.stats_lable.setText(
                f"last backup: {os.path.basename(os.path.split(self.dst_list[-1])[0])}")
        else:
            print("equal")
            self.ui.stats_lable.setText(
                f"last backup: {os.path.basename(os.path.split(self.dst_list[-1])[0])}")
        self.__clean_array()
        self.__zip_array()
        print("_timer_end_")

    def fancy_backup(self):
        # add backup option
        if not self.external.is_dir(self.src):
            QMessageBox.warning(
                self, "Warning", f"Something went wrong: \nsrc - {self.src} doesnt't exist", QMessageBox.Ok)
            if self.timer.isActive():
                self.timer.stop()
            return

        if not self.dst_list and self.external.is_dir(self.src):
            self.dst_list.append(self.external.create_name(self.src, self.dst))
            self.__backup__()
            self.ui.stats_lable.setText(
                f"last backup: {os.path.basename(os.path.split(self.dst_list[-1])[0])}")
            return

        if not self.external.cmp_folder(self.src, self.dst_list[-1], self.ignore_pattern):
            tmp_name = ""
            if self.count_fancy_backup > self.repeat:
                self.dst_list.append(
                    self.external.create_name(self.src, self.dst))
                self.count_fancy_backup = 0
                self.__backup__()
            else:
                tmp = self.external.create_name(self.src, self.dst, upd=True)
                tmp_name = self.dst[-1]
                self.external.rename_folder(tmp, self.dst_list[-1])
                self.dst_list[-1] = tmp
                self.count_fancy_backup += 1
                if not self.__backup__():
                    self.dst_list.append(tmp_name)
            self.ui.stats_lable.setText(
                f"last backup: {os.path.basename(os.path.split(self.dst_list[-1])[0])}")
        else:
            print("equal")

        self.__clean_array()
        self.__zip_array()
        print("_timer_end_")

    def update_time(self):
        # value = self.ui.time_holder.time().toPyTime()
        value = self.ui.timer_holder.value()
        self.ui.recovery_button.setVisible(False)
        self.time_for_timer = value*60*60  # tmp        

    def setup_recover(self):
        if self.dst_list:
            return_recover_src, ok = QInputDialog.getItem(
                self, 'Choose what to recover', 'List:', self.dst_list)
            if ok and return_recover_src:
                check_return = self.external.recover(return_recover_src, self.src)
                if check_return:
                    self.dst_list.remove(return_recover_src)
                    self.dst_list.append(check_return)
                    self.__clean_array()
                    self.__zip_array()
                    self.ui.recovery_button.setVisible(False)
                else:
                    QMessageBox.warning(
                        self, "Warning", f"Something went wrong:\n path status exists {return_recover_src} - {self.external.is_dir(return_recover_src)} \n{self.src} - {self.external.is_dir(self.src)} ", QMessageBox.Ok)
        else:
            QMessageBox.about(self, "No recover option",
                              "There's nothing to recover")

    def setup_backup(self):
        if self.timer.isActive():
            self.timer.stop()
            self.ui.tmp_button.setText("Start")
            self.backup_action.setText("Start backup")
            self.ui.recovery_button.setVisible(True)
        else:
            self.ignore_pattern.clear()
            for i in self.check_boxes:
                if i.isChecked():
                    self.ignore_pattern.append(i.text())
            if self.time_for_timer >= 0 and self.external.is_dir(self.ui.to_lable.text()) and self.external.is_dir(self.ui.from_lable.text()):
                self.src = self.ui.from_lable.text()
                self.dst = self.ui.to_lable.text()
                if not (self.src in self.dst or self.dst in self.src):
                    if self.time_for_timer == 0:
                        if self.ui.backup_option_1.isChecked():
                            self.backup()
                        if self.ui.backup_option_2.isChecked():
                            self.fancy_backup()
                        self.ui.recovery_button.setVisible(True)
                    else:
                        if self.ui.backup_option_1.isChecked():
                            self.timer.timeout.connect(self.backup)
                        if self.ui.backup_option_2.isChecked():
                            self.timer.timeout.connect(self.fancy_backup)

                        self.timer.setInterval(self.time_for_timer)
                        self.timer.start()
                        print(f"time {self.time_for_timer} src {
                              self.src} dst {self.dst}")
                        self.ui.tmp_button.setText("Stop")
                        self.backup_action.setText("Stop")

                else:
                    print(
                        f"(self.src in self.dst - {self.src in self.dst} or self.dst in self.src - {self.dst in self.src})")
                    QMessageBox.warning(self, "Warning", f"(self.src in self.dst - {
                                        self.src in self.dst} or self.dst in self.src - {self.dst in self.src})", QMessageBox.Ok)
                    self.ui.stats_lable.setText("Error")
            else:
                print('sad')
                QMessageBox.warning(
                    self, "Warning", f"Something went wrong: \ntimer is {self.timer.isActive()} \ntime interval: {self.time_for_timer} \nsrc: {self.src} \ndst {self.dst}", QMessageBox.Ok)
                print(
                    f"timer is {self.timer.isActive()} and it's because: {self.time_for_timer} or src {self.src} or dst {self.dst}")

    def __input_path(self, label: QLabel) -> None:
        """service function"""
        tmp = QFileDialog.getExistingDirectory(self, 'Select Folder')

        if not tmp:
            QMessageBox.warning(
                self, "Warning", "please select dir", QMessageBox.Ok)
        else:
            label.setText(tmp)

    # test close event

    def closeEvent(self, event):
        if self.ui.tray_check_box.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "AutoSaver",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                30
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
