from imports import *

class Gui(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title(TITLE)

		self.protocol("WM_DELETE_WINDOW", self._quit)

		self.notebook = widgets.VisualTabs(self)

	# TODO: remove it
	def _add(self, v):  # add or update
		tab = Frame(self.notebook)
		self.notebook.add(tab, text=v.name)
		self.notebook.pack()

		Label(tab, text="var 1").grid(row=0)
		var1 = DoubleVar()
		scale = Scale(tab, variable=var1)
		scale.grid(row=0, column=1)

		Label(tab, text="var 2").grid(row=1)
		var2 = DoubleVar()
		scale = Scale(tab, variable=var2 )
		scale.grid(row=1, column=1)
	#

	def update(self):
		Tk.update(self)
		self.notebook.update()

	def _quit(self):
		None

tk = Gui()

def update():
	tk.update()
