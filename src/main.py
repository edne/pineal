from imports import *
from visuals import *
from loader import *
from analyzer import Analyzer
import window

class MainClass:
	def __init__(self):
		
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
		
		self.win_master = window.Master(self)
		self.win_overview = window.Overview(self)
		
		self.visuals = Visuals(self)
		self.analyzer = Analyzer(self)
		self.loader = Loader(self)
		
		self.loader.start()
		self.analyzer.start()
		
		self._running = False
	
	def run(self):
		self._running = True
		
		try:
			glutMainLoop()
		except KeyboardInterrupt:
			None
		
		self._running = False
		
		self.loader.stop()
		self.analyzer.stop()
	
