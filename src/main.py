from imports import *
from visuals import *
from loader import *
from gui import *
from analyzer import Analyzer
from graphic import Graphic

class MainClass:
	def __init__(self):
		
		self.graphic = Graphic(self)
		
		self.visuals = Visuals(self)
		self.analyzer = Analyzer(self)
		self.loader = Loader(self)
		#self.gui = Gui(self)
		
		self.loader.start()
		self.analyzer.start()
		
		self._running = False  # dove la usavo?
		self._stop = False
	
	def run(self):
		self._running = True
		try:
			while not self._stop:
				self.graphic.update()
				#self.gui.update()
		except KeyboardInterrupt:
			None
		
		self._running = False
		
		self.loader.stop()
		self.analyzer.stop()
	
