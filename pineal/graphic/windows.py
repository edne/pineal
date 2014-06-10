from imports import *

postprocessing = ctypes.CDLL("pineal/postprocessing")

class Overview(pyglet.window.Window):
	def __init__(self, **args):
		pyglet.window.Window.__init__(self, **args)

		self.fps_display = pyglet.clock.ClockDisplay()


	def on_draw(self):
		self.clear()

		if rendering.texture:
			rendering.texture.blit(0,0,0, self.width,self.height)

		self.fps_display.draw()

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		camera.rotate(float(dx)/100, float(dy)/100)

	def on_key_press(self, symbol, modifiers):
		if symbol == key.DELETE:
			camera.reset()

		if symbol == key.W: camera.start_rotate(0,-1)
		if symbol == key.S: camera.start_rotate(0,1)
		if symbol == key.A: camera.start_rotate(1,0)
		if symbol == key.D: camera.start_rotate(-1,0)

		if symbol == key.UP: camera.start_move(-1)
		if symbol == key.DOWN: camera.start_move(1)


	def on_key_release(self, symbol, modifiers):
		if symbol == key.W: camera.stop_rotate(0,-1)
		if symbol == key.S: camera.stop_rotate(0,1)
		if symbol == key.A: camera.stop_rotate(1,0)
		if symbol == key.D: camera.stop_rotate(-1,0)

		if symbol == key.UP: camera.stop_move(-1)
		if symbol == key.DOWN: camera.stop_move(1)

class Rendering(pyglet.window.Window):
	def __init__(self, **args):
		pyglet.window.Window.__init__(self, **args)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glEnable( GL_VERTEX_ARRAY )

		glEnable( GL_LINE_SMOOTH )
		glEnable( GL_POLYGON_SMOOTH )
		glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )
		glHint( GL_POLYGON_SMOOTH_HINT, GL_NICEST )

		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glEnable(GL_COLOR_MATERIAL)
		glShadeModel(GL_SMOOTH)

		self.texture = None

	def on_draw(self):
		self.clear()
		predraw(*self.get_size())

		for v in visuals.get():
			glMatrixMode(GL_MODELVIEW)
			v.update()

		buf = pyglet.image.get_buffer_manager().get_color_buffer()

		rawimage = buf.get_image_data()
		pitch = rawimage.width * len('RGBA')
		pixels = rawimage.get_data('RGBA', pitch)

		# li controllo da gui e F.O.
		postprocessing.mirror(pixels, rawimage.width, rawimage.height)

		self.texture = rawimage.get_texture()


class Master(pyglet.window.Window):
	def __init__(self, **args):
		pyglet.window.Window.__init__(self, **args)

	def on_draw(self):
		self.clear()
		if rendering.texture:
			rendering.texture.blit(0,0,0, self.width,self.height)

def predraw(w,h):
	glLightfv(GL_LIGHT0, GL_POSITION,vec(1,1,10, 3))
	glLightModelfv(
		GL_LIGHT_MODEL_AMBIENT|GL_LIGHT_MODEL_TWO_SIDE,
		vec(1,1,1, 1.0)
	)

	glMatrixMode (GL_PROJECTION)
	glLoadIdentity()
	#glOrtho(-1, 1, -1, 1, -1, 1)
	#(w,h) = self.get_size()
	glScalef(
		float(min(w,h))/w,
		-float(min(w,h))/h,
		1
	)

	gluPerspective(45.0, 1, 0.1, 1000.0)
	gluLookAt(
		camera.x,
		camera.y,
		camera.z,
		0,0,0,
		camera.up[0],
		camera.up[1],
		camera.up[2]
	)

def create():
	global rendering, overview, master

	platform = pyglet.window.get_platform()
	display = platform.get_default_display()
	screens = display.get_screens()

	overview = Overview(
		caption = "Overview",
		width = 600, height = 450,
		vsync = 0
	)

	rendering = Rendering(
		caption = "Rendering",
		width = 640, height = 480,
		vsync = 0,
		visible = 0
	)

	master = Master(
		caption = "Master",
		screen=screens[-1],
		fullscreen = len(screens)>1,
		vsync = len(screens)>1,
		visible = len(screens)>1,
	)
	master.set_mouse_visible(False)
