import pickle

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
    return str

dict = {
        "Ctrl" : "^",
        "Win" : "#",
        "Alt" : "!",
        "Shift" : "+"
    }

test = hotkey(["A"], "OMGWTFBBQ", ["Ctrl"])
print(test.output())
with open("test.ahk", "w") as fp:
#     stuff
    printHeader(fp)
    fp.write(parseBasicOutput(test))
# with open("testpickle", "wb") as fp:
#     js = pickle.dumps(test)
#     fp.write(js)
with open("testpickle", "rb") as fp:
    obj = fp.read()
    obj = pickle.loads(obj)
    print(obj.output())