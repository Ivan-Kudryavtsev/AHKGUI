import pickle
import sys
import time

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QRegExp, QDir, Qt


class hotkey:
    # need input key(s), modifiers, output key
    # eventually move on to output functions probably and then parse those but that's too complicated right now
    inputKeys = []
    # what format are mods stored??
    modifiers = []
    outputKeys = []

    def __init__(self, inputs, output, mods):
        self.inputKeys = inputs
        print(inputs)
        self.outputKeys = output
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
        if (len(self.inputKeys) > 0 and self.outputKeys != [] and len(self.inputKeys) < 3):
            return True
        return False

    def getInput(self):
        str = ""
        for letter in self.inputKeys:
            str += letter
        return str

    def getOutput(self):
        str = ""
        for letter in self.outputKeys:
            str += letter
        return str

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

    def parseBasicOutput(self):
        str = ""
        for input in self.modifiers:
            str += dict.get(input)
        for input in self.inputKeys:
            str += input
        #     account for multiple?
        str += ":: Send, "
        str += self.getOutput();
        str += "\n\n"
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
            str += hotkey.parseBasicOutput()
        return str


class hotkeyMap():
    hotkeylists = []

    def __init__(self, hotkeyLists):
        self.hotkeyLists = hotkeyLists

    def addHotkeyList(self, hotkeys):
        self.hotkeyLists.append(hotkeys)

    def addDefaultHotkeyList(self):
        n = hotkeyList([], "Default")
        self.addHotkeyList(n)

    def removeHotkeyList(self, hotkeys):
        self.hotkeyLists.remove(hotkeys)

    def getListNames(self):
        string = []
        for list in self.hotkeyLists:
            string.append(list.window)
        return string

    def getLists(self):
        return self.hotkeyLists

    def findByWindow(self, windowName):
        for hotkeyList in self.hotkeyLists:
            if hotkeyList.window == windowName:
                return hotkeyList
        return None

    def parse(self):
        str = ""
        for hotkey in self.hotkeyLists:
            str += hotkey.parse()
            str += "\n"
        return str


def printHeader(file):
    file.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

""")


dict = {
    "CTRL": "^",
    "WIN": "#",
    "ALT": "!",
    "SHIFT": "+"
}


def unpickleObject(filename):
    with open(filename, "rb") as fp:
        obj = fp.read()
        obj = pickle.loads(obj)
        return obj


def pickleObject(filename, object):
    with open(filename, "wb") as fp:
        js = pickle.dumps(object)
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


class windowSelectorWidget(QWidget):
    # hang on this needs to handle quite a lot
    def __init__(self, hotkeyMap):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.hotkeyMap = hotkeyMap

        self.dropdown = QComboBox()
        for hotkeyList in hotkeyMap.hotkeyLists:
            self.dropdown.addItem(hotkeyList.window)
        self.dropdown.activated.connect(lambda: self.parent().parseDropdown(self.dropdown.currentText()))
        self.dropdown.setEditable(True)
        self.dropdown.setDuplicatesEnabled(False)



        # Define delete list button
        self.deleteListButton = QPushButton()
        self.deleteListButton.setText("Delete List")
        self.deleteListButton.pressed.connect(self.deleteCurrent)

        # Define new list button
        self.newListButton = QPushButton()
        self.newListButton.setText("New List")
        self.newListButton.pressed.connect(lambda: self.hotkeyMap.addDefaultHotkeyList())
        self.newListButton.pressed.connect(self.reload)
        self.newListButton.pressed.connect(lambda: self.parent().parseDropdown("Default"))


        # add layout elements
        self.layout.addStretch()
        self.layout.addWidget(self.deleteListButton)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.newListButton)
        self.layout.addStretch()


    def reload(self):
        # currentList = self.dropdown.currentText()
        self.dropdown.clear()
        self.dropdown.addItems(self.hotkeyMap.getListNames())
        if self.dropdown.findText("Default") == -1:
            self.dropdown.setCurrentIndex(0)
        else:
            self.dropdown.setCurrentIndex(self.dropdown.findText("Default"))


    def deleteCurrent(self):

        # self.layout.addWidget(q)
        msg = QMessageBox()
        msg.setWindowTitle("Confirm")
        msg.setText("Are you sure? Click OK to continue.")
        msg.setStandardButtons(QMessageBox.Cancel| QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setIcon(QMessageBox.Question)


        msg.buttonClicked.connect(self.popup_button_delete)

        x = msg.exec_()

    def print(self):
        print("STUFF")

    def popup_button_delete(self, i):
        print("AAA")
        print(i.text())
        if (i.text() == "OK"):
            current = self.dropdown.currentText()
            self.hotkeyMap.removeHotkeyList(self.hotkeyMap.findByWindow(current))
            self.dropdown.removeItem(self.dropdown.findText(current))
            self.reload()

    def getCurrent(self):
        # print("AAAAAAAAAAAAAAAAAAAAA")
        # print(self.dropdown.currentText())
        return self.dropdown.currentText()
    # def select(self,name):
    #     # select correct dropdown
    #     self.dropdown.


class hotkeyMapWidget(QWidget):
    def __init__(self, hotkeyMap):
        QWidget.__init__(self)
        self.hotkeyMap = hotkeyMap

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # windowName = QLabel()
        # windowName.setText(self.hotkeyList.window)

        windowNameWidget = windowSelectorWidget(hotkeyMap)
        self.layout.addWidget(windowNameWidget)
        windowName = windowNameWidget.getCurrent()
        list = hotkeyMap.findByWindow(windowName)


        if list is not None:
            widget = hotkeyListWidget(list)
            self.layout.addWidget(widget)
            self.currentList = widget
        else:
            label = QLabel()
            label.setText("CANNOT FIND THAT LIST")
            self.layout.addWidget(label)

    def parseDropdown(self, listName):
        if (listName == "Create new list"):
            print("NEW LIST")

        else:
            print(self.currentList.hotkeyList)
            self.currentList.removeButton()
            self.currentList.setParent(None)
            # self.layout.removeWidget(self.currentList)
            self.currentList = hotkeyListWidget(self.hotkeyMap.findByWindow(listName))
            self.layout.addWidget(self.currentList)

#       have the widget contain the


class hotkeyListWidget(QWidget):
    def __init__(self, hotkeyList):
        QWidget.__init__(self)
        self.hotkeyList = hotkeyList

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        for hotkey in hotkeyList.hotkeys:
            self.layout.addWidget(hotkeyWidget(hotkey))

        self.addButton()
        self.layout.addStretch()

    def getHotkeyList(self):
        return self.hotkeyList

    def removeButton(self):
        self.pushButton.setParent(None)
        # print("REMOVE BUTTON")

    def addHotkey(self):
        hkey = hotkey([],[],[])
        self.pushButton.setParent(None)
        self.layout.addWidget(hotkeyWidget(hkey))
        self.hotkeyList.addHotkey(hkey)
        self.addButton()
        # self.removeButton()

    def addButton(self):
        addButton = QPushButton()
        addButton.setText("New hotkey")
        # print("NEW BUTTON CREATED")
        addButton.clicked.connect(lambda: self.addHotkey())
        self.pushButton = addButton

        self.layout.addWidget(addButton)

class hotkeyWidget(QWidget):
    hotkey = ""

    # modList = []

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
        # needs to be reworked so that depends only on hotkey object!
        ch = dict.get(mod)
        # print(ch)
        if (ch in self.hotkey.modifiers):
            # self.modList.remove(ch)
            self.hotkey.modifiers.remove(ch)
        else:
            # self.modList.append(ch)
            self.hotkey.modifiers.append(ch)
        # print(self.modList)

    def __init__(self, hotkey):
        QWidget.__init__(self)
        self.hotkey = hotkey

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.lInput = capsLineEdit()
        self.lOutput = QLineEdit()
        # self.lInput.setText("INPUT")
        if (self.hotkey.inputKeys == []):
            self.lInput.setPlaceholderText("INPUT")
        else:
            self.lInput.setText(self.hotkey.getInput())
        if (self.hotkey.outputKeys == []):
            self.lOutput.setPlaceholderText("OUTPUT")
        else:
            self.lOutput.setText(self.hotkey.getOutput())

        # Define checkboxes for modifiers with text
        # Set checkboxes to existing value of hotkey
        self.chkCTRL = QCheckBox()
        self.chkCTRL.setText("CTRL")
        if "CTRL" in self.hotkey.modifiers:
            self.chkCTRL.setChecked(True)

        self.chkSHIFT = QCheckBox()
        self.chkSHIFT.setText("SHIFT")
        if "SHIFT" in self.hotkey.modifiers:
            self.chkSHIFT.setChecked(True)

        self.chkWIN = QCheckBox()
        self.chkWIN.setText("WIN")
        if "WIN" in self.hotkey.modifiers:
            self.chkWIN.setChecked(True)

        self.chkALT = QCheckBox()
        self.chkALT.setText("ALT")
        if "ALT" in self.hotkey.modifiers:
            self.chkALT.setChecked(True)

        # Bind changing checkbox state to changing state of hotkey object
        self.chkWIN.stateChanged.connect(lambda: self.toggleModState("WIN"))
        self.chkSHIFT.stateChanged.connect(lambda: self.toggleModState("SHIFT"))
        self.chkALT.stateChanged.connect(lambda: self.toggleModState("ALT"))
        self.chkCTRL.stateChanged.connect(lambda: self.toggleModState("CTRL"))

        # Add all widgets in order
        self.layout.addWidget(self.lInput)
        self.layout.addWidget(self.chkALT)
        self.layout.addWidget(self.chkCTRL)
        self.layout.addWidget(self.chkSHIFT)
        self.layout.addWidget(self.chkWIN)
        self.layout.addWidget(self.lOutput)
        self.layout.addStretch()

        # add validators for lineEdit objects
        twocharrgx = QRegExp(".{2}")
        twochar = QRegExpValidator(twocharrgx, self.lInput)
        self.lInput.setValidator(twochar)
        # self.hotkey.text = self.lInput.text()
        self.lInput.textChanged.connect(lambda: self.hotkey.setInput(self.lInput.text()))
        self.lOutput.textChanged.connect(lambda: self.hotkey.setOutput(self.lOutput.text()))
        self.adjustSize()


def printTest():
    print("TEST")


class mainwindow(QMainWindow):
    layout = ""

    def createActions(self):
        self.saveFile = QAction("&Save", self)
        self.saveFile.setToolTip("Save file")
        self.saveFile.triggered.connect(lambda: saveHotkeyList(self))

        self.openFile = QAction("&Open", self)
        self.openFile.triggered.connect(lambda: loadHotkeyList(self))

        self.exportFile = QAction("&Export", self)
        self.exportFile.triggered.connect(lambda: exportHotkeyList(self))

    def addWidget(self, widget):
        # widget.setParent(self)
        self.layout.addWidget(widget)
        # self.setLayout(self.layout)

    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)

        container = QWidget()
        self.setCentralWidget(container)
        self.layout = QVBoxLayout(container);
        self.setLayout(self.layout)

        self.createActions()

        mainMenu = QMenuBar()
        self.menu = mainMenu
        fileMenu = mainMenu.addMenu("File")
        editMenu = mainMenu.addMenu("Edit")

        #   create actions here and assign them

        fileMenu.addAction(self.saveFile)
        fileMenu.addAction(self.openFile)
        fileMenu.addAction(self.exportFile)

        self.setMenuBar(mainMenu)


def selectExistingFile(window):
    fname, _ = QFileDialog.getOpenFileName(window, 'TEST', "*.pkl")
    return fname


def selectNewPickleFile(window):
    fname, _ = QFileDialog.getSaveFileName(window, 'TEST', "*.pkl")
    return fname


def selectNewAHKFile(window):
    fname, _ = QFileDialog.getSaveFileName(window, 'TEST', "*.ahk")
    return fname


def openHotkeyList(window):
    name = selectExistingFile(window)
    if name == "":
        return None
    return unpickleObject(name)


def loadHotkeyList(window):
    # need to clear the window
    obj = openHotkeyList(window)
    if obj is None:
        return False

    for i in reversed(range(window.layout.count())):
        window.layout.itemAt(i).widget().setParent(None)

    for hotkeyList in obj.getLists():
        for hotkey in hotkeyList.hotkeys:
            hkey = hotkeyWidget(hotkey)
            window.addWidget(hkey)


def saveHotkeyList(window):
    name = selectNewPickleFile(window)
    # get open hotkeyList
    if name == "":
        return False
    pickleObject(name, currentLists)
    # how do i do that though...


def exportHotkeyList(window):
    name = selectNewAHKFile(window)
    if name == "":
        return False
    with open(name, "w") as fp:
        fp.write((currentLists.parse()))


def loadFile(fname, window):
    with open(fname, "rb") as fp:
        # print("Opened" + fname)
        lists = fp.read()
        lists = pickle.loads(lists)
        # print("Lists" + lists.parse())

        # loop not running for some reason
        widget = hotkeyMapWidget(lists)
        window.addWidget(widget)

        # for keylist in lists.getLists():
        #     # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        #     # print("FOUND" + keylist.parse())
        #     widget = hotkeyListWidget(keylist)
        #     window.addWidget(widget)

        return lists


def createTestFile():
    test1 = hotkey(["A"], list("TEST1"), ["CTRL"])
    test2 = hotkey(["B"], list("TEST2"), ["SHIFT"])
    test3 = hotkey(["A"], list("TEST3"), ["CTRL"])
    test4 = hotkey(["B"], list("TEST/"), ["SHIFT"])
    test5 = hotkey(["A"], list("TEST5"), ["CTRL"])
    test6 = hotkey(["B"], list("TEST6"), ["SHIFT"])
    list1 = hotkeyList([test1, test2, test3], "Notepad")
    list2 = hotkeyList([test4, test5, test6], "Chrome")
    nlist1 = hotkeyMap([list1, list2])
    # data = pickle.dumps(nlist1)
    # with open("testfile.pkl", "wb") as fp:
    #     fp.write(data)
    pickleObject("testfile.pkl", nlist1)


def main():
    createTestFile()

    # testlist = hotkeyList([], "Notepad")
    # test = hotkey(["A"], "OMGWTFBBQ", [])
    # test2 = hotkey(["B"], "HelpMePlease", [])
    # testlist.addHotkey(test)
    # testlist.addHotkey(test2)
    # writeToFile(testlist, "test.ahk")
    app = QApplication(sys.argv)
    win = mainwindow()
    win.setGeometry(300, 300, 300, 300)
    win.setWindowTitle("AHKGUI")
    # k = hotkeyListWidget(testlist)
    # win.addWidget(k)
    # fname, _ = QFileDialog.getOpenFileName(win, 'TEST', "*.pkl")
    # c = QPushButton()
    # c.setText("SAVE")
    # c.pressed.connect(lambda: pickleHotkeyList("tht.pkl", testlist))
    # win.addWidget(c)
    # b = QPushButton()
    # b.setText("SUBMIT")
    # b.pressed.connect(lambda: loadHotkeyList(win))

    # win.addWidget(b)

    global currentLists
    currentLists = loadFile("testfile.pkl", win)
    # print(currentLists.parse())
    win.show()

    # pickleHotkeyList("th.pkl", testlist)
    sys.exit(app.exec_())


main()
