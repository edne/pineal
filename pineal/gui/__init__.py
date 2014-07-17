from pineal.config import TITLE
from Tkinter import Tk
import widgets


class Gui(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(TITLE)

        self.protocol("WM_DELETE_WINDOW", self._quit)

        self.notebook = widgets.VisualTabs(self)

    def update(self):
        Tk.update(self)
        self.notebook.update()

    def _quit(self):
        None

tk = None  # TODO: that's HORRIBLE


def init():
    global tk
    tk = Gui()


def update():
    tk.update()
