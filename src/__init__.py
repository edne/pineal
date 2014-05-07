from imports import *

from graphic import Graphic
from visuals import Visuals
from loader import Loader
from analyzer import Analyzer
from gui import Gui

class Main:
	def __init__(self):
		self.graphic = Graphic()
		self.visuals = Visuals()
		__builtins__['visuals'] = self.visuals
		self.loader = Loader()
		self.analyzer = Analyzer()
		self.gui = Gui()
		
		self.loader.start()
		self.analyzer.start()
		
	def run(self):
		try:
			while True:
				self.analyzer.update()
				self.graphic.update()
				self.visuals.update()
				self.gui.update()
		except KeyboardInterrupt:
			None
		
		self.loader.stop()
		self.analyzer.stop()
	
