
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
        if (len(self.inputKeys) > 0 and self.outputKey != ""):
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


test = hotkey(["A, B, C"], "OMGWTFBBQ", ["Ctrl"])
print(test.output())

