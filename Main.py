print("Hello world")

class hotkey:
    # need input key(s), modifiers, output key
    # eventually move on to output functions probably and then parse those but that's too complicated right now
    inputKeys = []
    modifiers = []
    outputKey = None

    def __init__(self, inputs, output, mods):
        inputKeys = inputs
        outputKey = output
        modifiers = mods

    def isValid(self):
        if (len(self.inputKeys) > 0 and self.outputKey is not None):
            return True
        return False





