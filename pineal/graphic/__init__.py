from imports import *

from pyglet import clock

class Graphic:
	def __init__(self):
		glutInit(sys.argv)  # for the 3d presets
		windows.create()
	
	def update(self):
		dt = clock.tick()  # TODO get dt
		camera.update(dt)
		for window in pyglet.app.windows:
			window.switch_to()
			window.dispatch_events()
			window.dispatch_event('on_draw')
			window.flip()


graphic = Graphic()
def update():
	graphic.update()
