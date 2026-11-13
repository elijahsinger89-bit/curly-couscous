# Fake om.cad.gui: dialogs answer from SCRIPT (a list of callables taking the dialog, returning (ok, values)).
SCRIPT = []
SHOWN = []      # every dialog: (title, [(kind, label, options/default)])
BOXES = []
OUTPUT = []


class UIOutputWindow:
    ALL = 0


class MessageBoxType:
    INFORMATION = 0


def CleanOutput(w):
    OUTPUT.clear()


def WriteToOutput(t, w):
    OUTPUT.append(t)


def ProcessEvents():
    pass


def ShowMessageBox(kind, title, text):
    BOXES.append(text)


class InputDialog:
    def __init__(self, title):
        self.title = title
        self.fields = []
        self.labels = set()

    def _add(self, kind, label, extra):
        assert label not in self.labels, "duplicate label " + label
        self.labels.add(label)
        self.fields.append((kind, label, extra))

    def AddText(self, label, defaultValue=""):
        self._add("text", label, defaultValue)

    def AddBool(self, label, defaultValue=False):
        self._add("bool", label, defaultValue)

    def AddDropDown(self, label, options, defaultIndex=0):
        self._add("drop", label, (list(options), defaultIndex))

    def defaults(self):
        d = {}
        for kind, label, extra in self.fields:
            d[label] = extra[0][extra[1]] if kind == "drop" else extra
        return d

    def Show(self):
        SHOWN.append((self.title, list(self.fields)))
        if not SCRIPT:
            raise AssertionError("no scripted answer for dialog: " + self.title)
        return SCRIPT.pop(0)(self)
