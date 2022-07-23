import pickle
import sys
import time

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QRegExp, QDir



class hotkey:
    # need input key(s), modifiers, output key
    # eventually move on to output functions probably and then parse those but that's too complicated right now
    inputKeys = []
    modifiers = []
    outputKeys = []

    def __init__(self, inputs, output, mods):
        self.inputKeys = inputs
        print(inputs)
        self.outputKey = output
        print(output)
        self.modifiers = mods
        print(mods)

    def setInput(self, string):
        self.inputKeys = []
        for i in range(0, len(string)):
            self.inputKeys.append(string[i])
        print(self.inputKeys)

    def setOutput(self, string):
        self.outputKeys = []
        for i in range(0, len(string)):
            self.outputKeys.append(string[i])
        print(self.outputKeys)

    def isValid(self):
        if (len(self.inputKeys) > 0 and self.outputKey != "" and len(self.inputKeys) < 3):
            return True
        return False

    def createWidget(self):
        return hotkeyWidget(self)

    def output(self):
        str = "Modifiers: "
        for mod in self.modifiers:
            str += mod
            str += ", "
        str += "Inputs: "
        for input in self.inputKeys:
            str += input
            str += ", "
        str += "Output: "
        for output in self.outputKeys:
            str += output
            str += ", "
        return str

class hotkeyList():
    hotkeys = []
    window = ""

    def __init__(self, hotkeys, window):
        self.hotkeys = hotkeys
        self.window = window

    def addHotkey(self, hotkey):
        self.hotkeys.append(hotkey)

    def removeHotkey(self, hotkey):
        self.hotkeys.remove(hotkey)

    def parse(self):
        str = ""
        if self.window != "":
            str += "#IfWinActive ahk_class " + self.window + "\n"
        for hotkey in self.hotkeys:
            str += parseBasicOutput(hotkey)
        return str

def printHeader(file):
    file.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

""");

def parseBasicOutput(hotkey):
    str = ""
    for input in hotkey.modifiers:
        str += input
    for input in hotkey.inputKeys:
        str += input
    #     account for multiple?
    str += ":: Send, "
    str += hotkey.outputKey;
    str += "\n\n"
    return str

dict = {
        "CTRL" : "^",
        "WIN" : "#",
        "ALT" : "!",
        "SHIFT" : "+"
    }


def unpickleHotkeyList(filename):
    with open(filename, "rb") as fp:
        obj = fp.read()
        obj = pickle.loads(obj)
        return obj

def pickleHotkeyList(filename, hotkeys):
    with open(filename, "wb") as fp:
        js = pickle.dumps(hotkeys)
        fp.write(js)

def writeToFile(hotkeyList, filename):
    with open(filename, "w") as fp:
        printHeader(fp)
        fp.write(hotkeyList.parse())

class capsLineEdit(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)
        self.textChanged.connect(self.upCase)

    def upCase(self):
        self.setText(self.text().upper())

class hotkeyWidget(QWidget):
    hotkey = ""
    modList = []

    def getInput(self):
        return self.lInput

    def getOutput(self):
        return self.lOutput

    def getMods(self):
        str = ""
        if (self.chkWIN.isChecked()):
            str += "WIN"
        if (self.chkALT.isChecked()):
            str += "ALT"
        if (self.chkSHIFT.isChecked()):
            str += "SHIFT"
        if (self.chkCTRL.isChecked()):
            str += "CTRL"
        return str

    def toggleModState(self, mod):
        ch = dict.get(mod)
        # print(ch)
        if (ch in self.modList):
            self.modList.remove(ch)
            self.hotkey.modifiers.remove(ch)
        else:
            self.modList.append(ch)
            self.hotkey.modifiers.append(ch)
        # print(self.modList)

    def __init__(self, hotkey):
        QWidget.__init__(self)
        self.hotkey = hotkey

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.lInput = capsLineEdit()
        self.lOutput = QLineEdit()
        self.chkCTRL = QCheckBox()
        self.chkCTRL.setText("CTRL")
        self.chkSHIFT = QCheckBox()
        self.chkSHIFT.setText("SHIFT")
        self.chkWIN = QCheckBox()
        self.chkWIN.setText("WIN")
        self.chkALT = QCheckBox()
        self.chkALT.setText("ALT")
        # self.lInput.setText("INPUT")
        self.lInput.setPlaceholderText("INPUT")
        self.lOutput.setPlaceholderText("OUTPUT")
        self.layout.addWidget(self.lInput)
        self.layout.addWidget(self.chkALT)
        self.layout.addWidget(self.chkCTRL)
        self.layout.addWidget(self.chkSHIFT)
        self.layout.addWidget(self.chkWIN)
        self.chkWIN.stateChanged.connect(lambda: self.toggleModState("WIN"))
        self.chkSHIFT.stateChanged.connect(lambda: self.toggleModState("SHIFT"))
        self.chkALT.stateChanged.connect(lambda: self.toggleModState("ALT"))
        self.chkCTRL.stateChanged.connect(lambda: self.toggleModState("CTRL"))
        self.layout.addWidget(self.lOutput)

        # add validators for lineEdit objects!
        twocharrgx = QRegExp(".{2}")
        twochar = QRegExpValidator(twocharrgx, self.lInput)
        self.lInput.setValidator(twochar)
        # self.hotkey.text = self.lInput.text()
        self.lInput.textChanged.connect(lambda: self.hotkey.setInput(self.lInput.text()))
        self.lOutput.textChanged.connect(lambda: self.hotkey.setOutput(self.lOutput.text()))
        self.adjustSize()
#       define various ui elements based on hotkey values?

class mainwindow(QMainWindow):
    layout = ""

    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)

        container = QWidget()
        self.setCentralWidget(container)
        # using a widget as an argument in a Qt layout constructor results in
        # automatically setting the layout for that widget
        self.layout = QVBoxLayout(container);
        self.setLayout(self.layout)

    def addWidget(self, widget):
        # widget.setParent(self)
        self.layout.addWidget(widget)
        # self.setLayout(self.layout)



def selectFile(window):
    fname, _ = QFileDialog.getOpenFileName(window, 'TEST', "*.pkl")
    return fname

def openHotkeyList(window):
    return unpickleHotkeyList(selectFile(window))

def loadHotkeyList(window):
    # need to clear the window
    for i in reversed(range(window.layout.count())):
        window.layout.itemAt(i).widget().setParent(None)
    for hotkey in openHotkeyList(window).hotkeys:
        hkey = hotkeyWidget(hotkey)
        window.addWidget(hkey)



def main():
    testlist = hotkeyList([], "Notepad")
    test = hotkey(["A"], "OMGWTFBBQ", [])
    test2 = hotkey(["B"], "HelpMePlease", [])
    testlist.addHotkey(test)
    testlist.addHotkey(test2)
    # writeToFile(testlist, "test.ahk")
    app = QApplication(sys.argv)
    win = mainwindow()
    win.setGeometry(300,300,300,300)
    win.setWindowTitle("AHKGUI")
    n = hotkeyWidget(test)
    win.addWidget(n)
    h = hotkeyWidget(test2)
    win.addWidget(h)
    # fname, _ = QFileDialog.getOpenFileName(win, 'TEST', "*.pkl")


    b = QPushButton()
    b.setText("SUBMIT")
    b.pressed.connect(lambda: loadHotkeyList(win))
    win.addWidget(b)
    win.show()


    pickleHotkeyList("th.pkl", testlist)
    sys.exit(app.exec_())




main()