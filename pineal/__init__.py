from imports import *

def main():
	#
	# exaustive dependencies check
	#
	
	loader.start()
	analyzer.start()
	
	try:
		while True:
			gui.update()
			graphic.update()
	except KeyboardInterrupt:
		None
	
	loader.stop()
	analyzer.stop()
