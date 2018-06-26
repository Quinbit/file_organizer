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
        os.chdir("/")
        self.prev_text = ""
        self.title = 'HTML Highlighter'
        self.col_codes = {}
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 800

        self.initUI()

    def initUI(self):
        #We set the basic geometry of the window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Here we set up the button that will allow the user to find their html file of choice
        button = QPushButton('Find File', self)
        button.setToolTip('This button will allow you to select an html file to process')
        button.move(250,300)
        button.clicked.connect(self.on_click)

        #This button will allow the user to submit their predetermine color preferences
        col_button = QPushButton('Submit_color', self)
        col_button.move(250,550)
        col_button.clicked.connect(self.col_click)

        #This object will describe the drag and drop area for files
        drag_object = CustomLabel('Drag and file file here or press the find file button below\n          \
        to browse for your html text file', self)
        drag_object.move(130,50)

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

        #Where the user will enter in the colour of the tag
        self.textbox2 = QLineEdit(self)
        self.textbox2.setText("Type in color code")
        self.textbox2.move(160, 500)
        self.textbox2.resize(280,40)

        self.show()

    #returns the file that the user specified
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            return fileName
        else:
            return "Error"

    #looks for a file to get the html from
    @pyqtSlot()
    def on_click(self):
        print('Looking for file')
        location = self.openFileNameDialog()
        new_location = create_new_html(location, self)
        self.drag_object.setText("New html text file saved to: \n" + new_location)

    #Saves the user's input for tag colour
    @pyqtSlot()
    def col_click(self):
        tag = self.textbox.text().upper()
        col = self.textbox2.text().upper()
        self.prev_text = self.prev_text + "\n" + tag + " will have colour code " + col
        print(self.prev_text)
        self.res.setText(self.prev_text)
        self.col_codes[tag] = col

#Describes the hover area
class CustomLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setGeometry(parent.left // 2, parent.top // 2, parent.width // 1.5, parent.height // 3.0)

    def dragEnterEvent(self, e):
        print("File has entered the drop area")
        e.accept()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        self.move(100, 50)
        location = e.mimeData().text()
        new_location = create_new_html(location, self.parent)
        self.setText("New html text file saved to: \n" + new_location)
#Called when a new file is to be created
def create_new_html(location, gui_obj):
    location = location[8:]

    new_file = get_new_html_location(location)

    f = open(location, "r")

    text = f.read()

    content = mod_string(text, gui_obj)

    g = open(new_file, "w")

    g.write(content)
    g.close()
    f.close()

    return new_file

#Modifies the input string to give the corrected html string
def mod_string(string, gui_obj):
    code = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    tag_stack = [None]
    cur_color = ""
    i = 0

    #Cycles through all text in the file
    while (i < len(string)):
        new = ""
        if string[i] == "<":
            x = 1

            #Identifies the tag
            while(string[x+i] != ">"):
                new += string[x+i]
                x += 1

            #If the tag is the end tag end_statement will be true
            end_statement = ("/" in new )
            new = new.replace("/", "").upper()

            if (not end_statement):
                #Since break doesn't have any ending tags, it is treated differently
                if new == "BR":
                    end_statement = True

                #We essentially create a stack of all the tags to determine what color should be displayed
                tag_stack.append(new)

                #Determines if this tag has been encountered before
                if (gui_obj.col_codes.get(new.upper(), False)):
                    string = string[:i] + "\\color[" + gui_obj.col_codes.get(new) + ']' + string[i:]
                    i += len("\\color[" + gui_obj.col_codes.get(new) + ']')
                else:
                    col = ""
                    for n in range(6):
                        col += code[int(random() * 16)]

                    gui_obj.col_codes[new.upper()] = col
                    string = string[:i] + "\\color[" + col + ']' + string[i:]
                    i += len("\\color[" + col + ']')

            #If this is the ending tag
            if end_statement:
                tag_stack.remove(tag_stack[-1])
                new_tag = False

                if (len(string) > x+i+1):
                    test_string = string[x+i+1:]
                    test_string = test_string.replace("\n","")
                    test_string = test_string.replace(" ", "")
                    #tests to see if there is another tag that will immediately take over the color scheme
                    if test_string[0] == "<":
                        if test_string[1] != '/':
                            new_tag = True
                else:
                    new_tag = True

                #If there isn't any new tags coming up, we rely on the stack for the old tags for our color
                if not new_tag:
                    string = string[:i+x+1] + "\\color[" + gui_obj.col_codes.get(tag_stack[-1]) + ']' + string[1+i+x:]
                    i += len("\\color[" + gui_obj.col_codes.get(tag_stack[-1]) + ']')
        i += 1

    print(gui_obj.col_codes)
    return string

#Gets the string for the location of the modified html file
def get_new_html_location(location):
    location = location.split("/")
    location.remove(location[-1])
    location.append("output.txt")
    location = reduce(lambda x,y: x+'/'+y, location)

    return location


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
