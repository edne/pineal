from imports import *
from pyglet.window import mouse
from pyglet.window import key

class Graphic:
	def __init__(self, parent):
		self.parent = parent
		
		print "init graphic"
		glutInit(sys.argv)  # for the 3d presets
		
		platform = pyglet.window.get_platform()
		display = platform.get_default_display()
		screens = display.get_screens()
		
		self.fps_display = pyglet.clock.ClockDisplay()
		
		self.overview = Overview(
			parent,
			caption = "Overview",
			width = 600, height = 450,
			vsync=0
		)
		
		self.master = Master(
			parent,
			caption = "Master",
			screen=screens[-1],
			fullscreen = len(screens)>1,
			vsync=1,
			visible = len(screens)>1
		)
		self.master.set_mouse_visible(False)
		
		self.size = self.master.get_size() if len(screens)>1 else (800,600)
		
		self.camera = Camera()
		
		self._stop = False
	
	def run(self):
		while not self._stop:
			
			pyglet.clock.tick()
			for window in pyglet.app.windows:
				window.switch_to()
				window.dispatch_events()
				window.dispatch_event('on_draw')
				window.flip()


class Camera:
	def __init__(self):
		self.r = (4.0/3)/math.tan(45.0/2)
		self.up = [0,1,0]
		
		self.ang_x = 0
		self.ang_y = 0
		self.rotate(0,0)
	
	def rotate(self, dx, dy):
		#ang_x = math.atan2(self.x, self.z)  # 0 on z axis
		#ang_y = math.atan2(self.y, self.z)
		
		self.ang_x -= float(dx)/100
		self.ang_y += float(dy)/100
		
		self.x = self.r * math.sin(self.ang_x)
		self.y = self.r * math.sin(self.ang_y)
		self.z = self.r * math.cos(self.ang_x)*math.cos(self.ang_y)
		
		self.up[1] = math.cos(self.ang_y)

class Overview(pyglet.window.Window):
	def __init__(self, parent, **args):
		self.parent = parent
		pyglet.window.Window.__init__(self, **args)
		
		self.fps_display = pyglet.clock.ClockDisplay()
		
		
	def on_draw(self):
		self.clear()
		
		self.parent.graphic.master.switch_to()
		buf = pyglet.image.get_buffer_manager().get_color_buffer()
		tex = buf.get_texture()
		self.switch_to()
		
		tex.blit(0,0,0, self.width,self.height)
		
		self.fps_display.draw()
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.parent.graphic.camera.rotate(dx, dy)
	
	def on_key_press(symbol, modifiers):
		None
    
class Master(pyglet.window.Window):
	def __init__(self, parent, **args):
		self.parent = parent
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
		
	
	def on_draw(self):
		self.clear()
		
		glLightfv(GL_LIGHT0, GL_POSITION,vec(1,1,10, 3))
		glLightModelfv(
			GL_LIGHT_MODEL_AMBIENT|GL_LIGHT_MODEL_TWO_SIDE,
			vec(1,1,1, 1.0)
		)
		
		glMatrixMode (GL_PROJECTION)
		glLoadIdentity()
		#glOrtho(-1, 1, -1, 1, -1, 1)
		(w,h) = self.parent.graphic.size
		glScalef(
			float(min(w,h))/w,
			-float(min(w,h))/h,
			1
		)
		
		camera = self.parent.graphic.camera
		
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
		
		self.parent.visuals.update()
		
