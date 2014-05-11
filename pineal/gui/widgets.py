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

            tab.update()


class Tab(Frame):
    def __init__(self, parent, v):
        Frame.__init__(self, parent)
        Notebook.add(parent, self, text=v.name)
        parent.pack()

        self.parent = parent
        self.v = v

        self.sliders = dict()

    def update(self):
        for key in self.v.box.var.keys():
            if not key in self.sliders.keys():
                slider = Slider(
                    self,
                    key,
                    len(self.sliders),
                    self.v.box.var[key]
                )
                self.sliders[key] = slider


class Slider:
    def __init__(self, parent, key, index, value=0.0):

        label = Label(parent, text=key)
        label.grid(row=index)

        self.var = DoubleVar()
        self.var.set(min(1.0, max(0.0, value)))
        self.var.trace("w", self.callback)

        scale = Scale(parent, variable=self.var)
        scale.grid(row=index, column=1)

        self.parent = parent
        self.key = key

    def callback(self, *args):
        visuals.reciver(
            self.parent.v.name,
            self.key,
            self.var.get()
        )
