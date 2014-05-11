from imports import *

class VisualTabs(Notebook):
    def __init__(self, parent):
        Notebook.__init__(self, parent)
        self.tabs = list()

    def add(self, v):
        tab = Tab(self, v)
        self.tabs.append(tab)

    def remove(self, tab):
        self.forget(tab)
        self.tabs.remove(tab)
        del tab

    def update(self):
        for v in visuals.get():
            if not v in [tab.v for tab in self.tabs]:
                self.add(v)

        for tab in self.tabs:
            if not tab.v in visuals.get():
                self.remove(tab)


class Tab(Frame):
    def __init__(self, parent, v):
        Frame.__init__(self, parent)
        Notebook.add(parent, self, text=v.name)
        parent.pack()

        self.v = v
