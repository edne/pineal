import Tkinter
import ttk


class VisualTabs(ttk.Notebook):
    def __init__(self, parent):
        self.parent = parent

        ttk.Notebook.__init__(self, parent)
        self.tabs = list()

    def add(self, v):
        tab = Tab(self, v)
        self.tabs.append(tab)

    def remove(self, tab):
        self.forget(tab)
        self.tabs.remove(tab)
        del tab

    def update(self):
        for v in self.parent.visuals.values():
            if v not in [tab.v for tab in self.tabs]:
                self.add(v)

        for tab in self.tabs:
            if tab.v not in self.parent.visuals.values():
                self.remove(tab)

            tab.update()


class Tab(ttk.Frame):
    def __init__(self, parent, v):
        self.parent = parent

        ttk.Frame.__init__(self, parent)
        ttk.Notebook.add(parent, self, text=v.name)
        parent.pack(fill=Tkinter.BOTH, expand=1)

        self.parent = parent
        self.v = v

        self.sliders = dict()

    def update(self):
        for key in self.v.box.var.keys():
            if key not in self.sliders.keys():
                slider = Slider(
                    self,
                    key,
                    len(self.sliders),
                    self.v.box.var[key]
                )
                self.sliders[key] = slider


class Slider:
    def __init__(self, parent, key, index, value=0.0):
        self.parent = parent

        label = ttk.Label(parent, text=key)
        label.grid(row=index)

        self.var = Tkinter.DoubleVar()
        self.var.set(min(1.0, max(0.0, value)))
        self.var.trace("w", self.callback)

        parent.grid_columnconfigure(1, weight=1)
        scale = ttk.Scale(parent, variable=self.var)
        scale.grid(row=index, column=1, sticky=Tkinter.E+Tkinter.W)

        self.parent = parent
        self.key = key

    def callback(self, *args):
        self.parent.visuals.reciver(
            self.parent.v.name,
            self.key,
            self.var.get()
        )
