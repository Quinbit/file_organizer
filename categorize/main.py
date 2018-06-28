import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QLineEdit, QLabel, QComboBox
from PyQt5.QtGui import QIcon
import os
from functools import reduce
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QMessageBox
from random import random

def parse_for_hidden(files):
    deleted = 0
    for i in range(len(files)):
        if len(files[i-deleted]) < 1:
            del files[i-deleted]
            deleted += 1
        elif files[i-deleted][0]=='.':
            del files[i-deleted]
            deleted += 1

    return files

class App(QWidget):
    def __init__(self):
        #here we initialize the basic parameters for the gui
        super().__init__()
        self.prev_text = ""
        self.title = 'Categorizer'
        self.col_codes = {}
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800
        self.cur_dir = os.getcwd()
        self.title_font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        self.base_dir = ""

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
        self.selected_file.setFont(self.title_font)
        self.selected_file.move(500, 100)

        self.directory_label = QLabel(self)
        self.directory_label.setText("Root Directory: " + self.base_dir)
        self.directory_label.move(500, 40)

        self.change_dir = QPushButton("Change Directory", self)
        self.change_dir.setToolTip("Click to change root directory")
        self.change_dir.move(900 + len(self.directory_label.text()), 40)
        self.change_dir.clicked.connect(self.change_dir_function)

        self.combo = QComboBox(self)
        self.combo.move(500, 200)
        self.combo.setToolTip("Choose which folder to add the designated file to")

        self.combo_hint = QLabel(self)
        self.combo_hint.setText("Folders")
        self.combo_hint.move(500, 170)

        self.add_folder = QPushButton("Add-->", self)
        self.add_folder.setToolTip("Press to add the folder to the collection of folders")
        self.add_folder.move(650, 200)

        self.added_folders = AddedFiles("", self)

        l = QLabel(self)
        l.setText("Files/Directories")
        l.move(100,100)

        self.show()
        self.getBaseDir()

    @pyqtSlot()
    def add_folder(self):
        pass

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

    def getBaseDir(self):
        if not os.path.isdir(os.getcwd() + "/.hidden"):
            self.buildDirPopup()
        else:
            self.base_dir = os.getcwd()
            self.directory_label.setText("Root Directory: " + self.base_dir)
            self.directory_label.adjustSize()
            self.drag_object.update_dir()
            self.change_dir.move(900 + len(self.directory_label.text()), 40)
        self.update_combo_box()

    def buildDirPopup(self):
        self.dirPopup = DirectoryPopup(self)

    def change_dir_function(self):
        fileName = str(QFileDialog.getExistingDirectory(self,"QFileDialog.getOpenFileName()"))

        if fileName:
            print(fileName)

            if os.path.isdir(fileName):
                os.chdir(fileName)
                self.getBaseDir()

    def update_combo_box(self):
        self.combo.clear()
        if self.base_dir != "":
            files = self.return_directories(self.base_dir, "")
            print(files)
            self.combo.addItems(files)
            self.adjustSize()

    def return_directories(self, dir, prefix):
        files = parse_for_hidden(os.listdir(dir))
        deleted = 0

        for i in range(len(files)):
            if os.path.isdir(dir+"/"+files[i-deleted]):
                files += self.return_directories(dir+"/"+files[i-deleted], files[i-deleted])
                files[i - deleted] = prefix + "/" + files[i - deleted]
            else:
                del files[i - deleted]
                deleted += 1

        return files


class CustomLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parent = parent
        self.max_length = 15
        self.setAcceptDrops(True)
        self.setGeometry(20, 20, 300, 500)
        self.setStyleSheet("border:1px solid rgb(0, 0, 0);")
        files = parse_for_hidden(os.listdir(os.getcwd()))
        self.elem = []

        if len(files) < self.max_length:
            files += [""]*(self.max_length-len(files))

        for i in range(len(files)):
            self.elem.append(ListElement(files[i], self, (30, 30+30*i)))

        #add back button
        self.back = QPushButton(" <--", self)
        self.back.setToolTip('Go up a directory')
        self.back.move(0,0)
        self.back.clicked.connect(self.back_function)

    @pyqtSlot()
    def back_function(self):
        os.chdir("..")
        self.parent.cur_dir = os.getcwd()
        self.update_dir()

    def dragEnterEvent(self, e):
        print("File has entered the drop area")
        e.accept()

    def dropEvent(self, e):
        #e.mimeData().text()
        fileName = e.mimeData().text()
        self.parent.cur_file = fileName
        self.parent.selected_file.setText("The selected file is: " + self.parent.cur_file)
        self.parent.selected_file.adjustSize()

    def update_dir(self):
        files = parse_for_hidden(os.listdir(os.getcwd()))

        if len(files) < self.max_length:
            files += [""]*(self.max_length-len(files))

        for i in range(len(self.elem)):
            self.elem[i].setText(files[i])
            self.elem[i].adjustSize()

class ListElement(QPushButton):
    def __init__(self, title, parent, pos):
        super().__init__(title, parent)
        self.parent = parent
        self.setAutoFillBackground(True)
        self.move(pos[0], pos[1])
        self.setStyleSheet("border:0px solid rgb(0, 0, 0);")
        self.clicked.connect(self.click)

    def enterEvent(self, QEvent):
        if self.text() != "":
            self.setStyleSheet("color: rgb(230, 230, 230); background-color: rgb(0,0,0); border:0px solid rgb(0, 0, 0);")

    def leaveEvent(self, QEvent):
        if self.text() != "":
            self.setStyleSheet("color: rgb(0,0,0); background-color: rgb(230,230,230); border:0px solid rgb(0, 0, 0);")

    @pyqtSlot()
    def click(self):
        print(self.parent.parent.cur_file)

        if not os.path.isdir(self.parent.parent.cur_dir + "/" + self.text()):
            self.parent.parent.cur_file = self.parent.parent.cur_dir + "/" + self.text()
            self.parent.parent.selected_file.setText("The selected file is: " + self.parent.parent.cur_file)
            print("The selected file is: " + self.parent.parent.cur_file)
            self.parent.parent.selected_file.adjustSize()
        else:
            os.chdir(self.parent.parent.cur_dir + "/" + self.text())
            self.parent.parent.cur_dir = self.parent.parent.cur_dir + "/" + self.text()
            self.parent.update_dir()


class DirectoryPopup(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.title = 'Select Root Directory'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 400
        self.parent = parent
        self.directory = os.getcwd()

        self.initUI()

        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #set into label
        self.intro = QLabel(self)
        self.intro.setText("This directory was not found to be a root directory\n\n please select a directory to use as the root")
        self.intro.move(self.width//4,10)

        self.confirm = QPushButton("Confirm", self)
        self.confirm.setToolTip("Click to confirm your root directory. By default it will be your current directory")
        self.confirm.move(self.width//(3.5), self.height//(4/3))
        self.confirm.clicked.connect(self.confirm_func)

        self.find = QPushButton("Find", self)
        self.find.setToolTip("Click to find a new directory to select as your root")
        self.find.move(self.width//(1.8), self.height//(4/3))
        self.find.clicked.connect(self.choose_dir)

        self.chosen_dir = QLabel(self)
        self.chosen_dir.setText("Selected Directory: " + self.directory)
        self.chosen_dir.move(self.width // 2 - 6*len("Selected Directory: " + self.directory)//2, self.height//2)

    def confirm_func(self, event):
        self.parent.base_dir = self.directory
        self.parent.cur_dir = self.directory
        os.chdir(self.directory)
        self.parent.drag_object.update_dir()
        self.parent.directory_label.setText("Root Directory: " + self.parent.base_dir)
        self.parent.directory_label.adjustSize()
        self.parent.update_combo_box()
        if not os.path.isdir(self.directory + "/.hidden"):
            os.system("mkdir " + self.directory + "/.hidden")
        self.close()

    def choose_dir(self, event):
        fileName = str(QFileDialog.getExistingDirectory(self,"QFileDialog.getOpenFileName()"))

        if fileName:
            print(fileName)

            if os.path.isdir(fileName):
                self.directory = fileName
                self.chosen_dir.setText("Selected Directory: " + self.directory)
                self.chosen_dir.adjustSize()

class AddedFiles(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parent = parent
        self.max_length = 15
        self.width = 200
        self.height = 600
        self.top = 200
        self.left = 800
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("border:1px solid rgb(0, 0, 0);")

    def initialize_elements(self):
        pass

    def add_element(self):
        pass

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
