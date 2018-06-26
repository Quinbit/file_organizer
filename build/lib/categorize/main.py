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
        self.prev_text = ""
        self.title = 'HTML Highlighter'
        self.col_codes = {}
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800

        self.initUI()

    def initUI(self):
        #We set the basic geometry of the window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Here we set up the button that will allow the user to find their html file of choice
        button = QPushButton('Find File', self)
        button.setToolTip('This button will allow you to select an html file to process')
        button.move(250,900)
        button.clicked.connect(self.on_click)

        #This button will allow the user to submit their predetermine color preferences

        drag_object = CustomLabel('Loading files in current directory...', self)
        drag_object.move(70,150)

        self.button = button
        self.drag_object = drag_object

        #This label will give the user the intructions needed
        instr = QLabel(self)
        instr.setText("To manually predefine a highlight color, type in the tag \nand the desired \
colour code in the two text boxes below")
        instr.move(130, 350)

        #This label will list all of the label colours that the user has specified
        res = QLabel(self)
        res.setText("")
        res.move(130, 600)
        res.resize(300, 200)

        self.res = res

        #Where the user will enter in the tag
        self.textbox = QLineEdit(self)
        self.textbox.setText("Type in html tag without brackettes")
        self.textbox.move(160, 450)
        self.textbox.resize(280,40)

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
            return fileName
        else:
            return "Error"

class CustomLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.move
        self.setGeometry(20, 20, 300, 500)
        self.setStyleSheet("border:1px solid rgb(0, 0, 0);")
        files = os.listdir(os.getcwd())
        self.setText("\n\n".join(files))

    def dragEnterEvent(self, e):
        print("File has entered the drop area")
        e.accept()

    def dropEvent(self, e):
        #e.mimeData().text()
        location = e.mimeData().text()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
