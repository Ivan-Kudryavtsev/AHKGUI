import pickle
import sys

import PyQt5
from PyQt5.QtWidgets import *


class hotkey:
    # need input key(s), modifiers, output key
    # eventually move on to output functions probably and then parse those but that's too complicated right now
    inputKeys = []
    modifiers = []
    outputKey = ""

    def __init__(self, inputs, output, mods):
        self.inputKeys = inputs
        print(inputs)
        self.outputKey = output
        print(output)
        self.modifiers = mods
        print(mods)


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
        str += self.outputKey
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


# class modifier:
#     modDict = {
#         "Ctrl" : "^",
#         "Win" : "#",
#         "Alt" : "!",
#         "Shift" : "+"
#     }
#
#     def returnKey(self, key):
#         return self.modDict[key]



def printHeader(file):
    file.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

""");


def parseBasicOutput(hotkey):
    str = ""
    for input in hotkey.modifiers:
        str += dict[input]
    for input in hotkey.inputKeys:
        str += input
    #     account for multiple?
    str += ":: Send, "
    str += hotkey.outputKey;
    str += "\n\n"
    return str

dict = {
        "Ctrl" : "^",
        "Win" : "#",
        "Alt" : "!",
        "Shift" : "+"
    }


def unpickleHotkeyList(filename):
    with open(filename, "rb") as fp:
        obj = fp.read()
        obj = pickle.loads(obj)
        return obj


def pickleHotkeyList(filename, hotkeys):
    with open(filename, "wb") as fp:
        js = pickle.dumps(hotkey)
        fp.write(js)

def writeToFile(hotkeyList, filename):
    with open(filename, "w") as fp:
        printHeader(fp)
        fp.write(hotkeyList.parse())

class hotkeyWidget(QWidget):
    hotkey = ""

    def __init__(self, hotkey):
        QWidget.__init__(self)
        self.hotkey = hotkey

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        lInput = QLineEdit()
        lOutput = QLineEdit()
        chkCTRL = QCheckBox()
        chkCTRL.setText("CTRL")
        chkSHIFT = QCheckBox()
        chkSHIFT.setText("SHIFT")
        chkWIN = QCheckBox()
        chkWIN.setText("WIN")
        chkALT = QCheckBox()
        chkALT.setText("ALT")
        lInput.setText("INPUT")
        lOutput.setText("OUTPUT")
        self.layout.addWidget(lInput)
        self.layout.addWidget(chkALT)
        self.layout.addWidget(chkCTRL)
        self.layout.addWidget(chkSHIFT)
        self.layout.addWidget(chkWIN)


        self.layout.addWidget(lOutput)

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

def main():
    testlist = hotkeyList([], "Notepad")
    test = hotkey(["A"], "OMGWTFBBQ", ["Ctrl"])
    test2 = hotkey(["B"], "HelpMePlease", ["Ctrl", "Shift"])
    testlist.addHotkey(test)
    testlist.addHotkey(test2)
    writeToFile(testlist, "test.ahk")
    app = QApplication(sys.argv)
    win = mainwindow()
    win.setGeometry(300,300,300,300)
    win.setWindowTitle("AHKGUI")
    n = hotkeyWidget(test)
    win.addWidget(n)
    h = hotkeyWidget(test2)
    win.addWidget(h)
    win.show()
    print(test.output())
    sys.exit(app.exec_())



main()