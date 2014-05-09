from imports import *

class Graphic:
	def __init__(self):
		glutInit(sys.argv)  # for the 3d presets
		windows.create()
	
	def update(self):
		pyglet.clock.tick()
		for window in pyglet.app.windows:
			window.switch_to()
			window.dispatch_events()
			window.dispatch_event('on_draw')
			window.flip()


graphic = Graphic()
def update():
	graphic.update()
