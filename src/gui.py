from imports import *

from Tkinter import *
from ttk import *

class Gui(Tk):
	def __init__(self):
		Tk.__init__(self)
		
		self.protocol("WM_DELETE_WINDOW", self._quit)
		
		self.note = Notebook(self)
		
	
	def add(self, v):  # add or update
		tab = Frame(self.note)
		self.note.add(tab, text=v.name)
		self.note.pack()
		
		#Label(tab, text="var 1").grid(row=0)
		#var1 = DoubleVar()
		#scale = Scale(tab, variable=var1)
		#scale.grid(row=0, column=1)
		
		#Label(tab, text="var 2").grid(row=1)
		#var2 = DoubleVar()
		#scale = Scale(tab, variable=var2 )
		#scale.grid(row=1, column=1)
	
	def update(self):
		Tk.update(self)
		
		names = visuals.names()
		tabs = self.note.tabs()
		
		for tab in tabs:
			name = self.note.tab(tab, "text")
			
			# remove deleted
			if not name in names:
				self.note.forget(tab)
			
			# update vars
			# elimina gli slider di variabili tolte
			# aggiorna i valori delle variabili (dizionario v.var)
			# crea i nuovi slider
			v = visuals.get(name)
			
			
		
		# add new ones
		for name in names:
			if not name in [self.note.tab(t, "text") for t in tabs]:
					self.add(visuals.get(name))
		
	
	def _quit(self):
		None
	
