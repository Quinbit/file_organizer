import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
import os
from functools import reduce
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QMessageBox
from random import random

class App(QWidget):
    def __init__(self):
        #here we initialize the basic parameters for the gui
        super().__init__()
        self.prev_text = "                           "
        self.title = 'HTML Highlighter'
        self.col_codes = {}
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800
        self.base_dir = os.getcwd()

        self.initUI()

    def initUI(self):
        #We set the basic geometry of the window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Here we set up the button that will allow the user to find their html file of choice
        button = QPushButton('Find File', self)
        button.setToolTip('This button will allow you to select an html file to process')
        button.move(150,700)
        button.clicked.connect(self.on_click)

        #This button will allow the user to submit their predetermine color preferences

        drag_object = CustomLabel('', self)
        drag_object.move(75,150)

        self.button = button
        self.drag_object = drag_object


        self.cur_file = ""
        self.selected_file = QLabel(self)
        self.selected_file.setText("The selected file is: " + self.cur_file)
        self.selected_file.move(500, 100)

        l = QLabel(self)
        l.setText("Files/Directories")
        l.move(100,100)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('Looking for file')
        location = self.openFileNameDialog()
        #do stuff

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

            self.cur_file = fileName
            self.selected_file.setText("The selected file is: " + self.cur_file)
            self.selected_file.adjustSize()

            return fileName
        else:
            return "Error"

class CustomLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setGeometry(20, 20, 300, 500)
        self.setStyleSheet("border:1px solid rgb(0, 0, 0);")
        files = os.listdir(os.getcwd())
        self.elem = []

        for i in range(len(files)):
            self.elem.append(ListElement(files[i], self, (30, 30+30*i)))

    def dragEnterEvent(self, e):
        print("File has entered the drop area")
        e.accept()

    def dropEvent(self, e):
        #e.mimeData().text()
        location = e.mimeData().text()

    def update_dir(self):
        files = os.listdir(os.getcwd())
        print(files)
        for i in range(len(self.elem)):
            self.elem[0].deleteLater()
        del self.elem[:]

        for i in range(len(files)):
            self.elem.append(ListElement(files[i], self, (30, 30+30*i)))

class ListElement(QPushButton):
    def __init__(self, title, parent, pos):
        super().__init__(title, parent)
        self.parent = parent
        self.setAutoFillBackground(True)
        self.move(pos[0], pos[1])
        self.setStyleSheet("border:0px solid rgb(0, 0, 0);")
        self.clicked.connect(self.click)

    def enterEvent(self, QEvent):
        self.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0,0,0); border:0px solid rgb(0, 0, 0);")

    def leaveEvent(self, QEvent):
        self.setStyleSheet("color: rgb(0,0,0); background-color: rgb(255,255,255); border:0px solid rgb(0, 0, 0);")

    @pyqtSlot()
    def click(self):
        print(self.parent.parent.cur_file)

        if not os.path.isdir(self.parent.parent.base_dir + "/" + self.text()):
            self.parent.parent.cur_file = self.parent.parent.base_dir + "/" + self.text()
            self.parent.parent.selected_file.setText("The selected file is: " + self.parent.parent.cur_file)
            print("The selected file is: " + self.parent.parent.cur_file)
            self.parent.parent.selected_file.adjustSize()
        else:
            os.chdir(self.parent.parent.base_dir + "/" + self.text())
            self.parent.parent.base_dir = self.parent.parent.base_dir + "/" + self.text()
            self.parent.update_dir()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
