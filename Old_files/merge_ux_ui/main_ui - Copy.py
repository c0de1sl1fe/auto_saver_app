import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5.QtGui import QMovie

from sidebar import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

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

