from imports import *

def main():
	loader.start()
	analyzer.start()
	
	try:
		while True:
			analyzer.update()
			graphic.update()
			visuals.update()
			gui.update()
	except KeyboardInterrupt:
		None
	
	loader.stop()
	analyzer.stop()
