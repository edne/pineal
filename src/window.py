from imports import *

class Window:
	def __init__(
		self, parent, title, resolution,
		smooth=True, hide_mouse=True,
	):
		self.parent = parent
		
		glutInitWindowSize(resolution[0], resolution[1])
		glutCreateWindow(title)
		
		glutReshapeFunc(self.reshape)
		glutDisplayFunc(self.update)
		glutCloseFunc(self.close)
		
		if hide_mouse:
			glutSetCursor(GLUT_CURSOR_NONE)
		else:
			glutSetCursor(GLUT_CURSOR_INHERIT)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glEnable( GL_VERTEX_ARRAY )
		
		if smooth:
			glEnable( GL_LINE_SMOOTH )
			glEnable( GL_POLYGON_SMOOTH )
			#glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )
			#glHint( GL_POLYGON_SMOOTH_HINT, GL_NICEST )
			glHint( GL_LINE_SMOOTH_HINT, GL_FASTEST )
			glHint( GL_POLYGON_SMOOTH_HINT, GL_FASTEST )
		
		glutSetOption(
			GLUT_ACTION_ON_WINDOW_CLOSE,
			GLUT_ACTION_CONTINUE_EXECUTION
		)
		
	
	def close(self):
		None
	
	def update(self):
		glClearColor(0, 0, 0, 1)
		#glClearColor(0, 0, 0, 0)
		#glClear(GL_COLOR_BUFFER_BIT)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		self.parent.visuals.update()
		
		glutSwapBuffers()
		glutPostRedisplay()
	
	def reshape(self, w,h):
		#glutReshapeWindow( w,h )
		
		#(w,h) = RESOLUTION
		
		glViewport(0, 0, w, h)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-1, 1, -1, 1, -1, 1)
		
		glScalef(
			float(min(w,h))/w,
			-float(min(w,h))/h,
			1
		)

class Master(Window):
	def __init__(self, parent):
		Window.__init__(self, parent, TITLE, RESOLUTION)
		self.lastTime = time.time()
	
	def close(self):
		self.parent._running = False
		glutLeaveMainLoop()
	
	def update(self):
		newTime = time.time()
		if newTime != self.lastTime:
			#sys.stdout.write(str(newTime-self.lastTime)+"ms   \r")
			print ("%dms       %.1ffps                \r" % (
				(newTime-self.lastTime)*1000,
				1.0/(newTime-self.lastTime)
			)),
		else:
			print ("0ms       inf fps                \r"),
		self.lastTime = newTime
		
		Window.update(self)

class Overview(Window):
	def __init__(self, parent):
		Window.__init__(
			self, parent,
			"Overview",
			(RESOLUTION[0]*3/4, RESOLUTION[1]*3/4),
			smooth = True, hide_mouse=False
		)
	
	def close(self):
		if self.parent._running:
			self.parent.win_overview = Overview(self.parent)
	
	def reshape(self, w,h):
		if h != w*RESOLUTION[1]/RESOLUTION[0]:
			glutReshapeWindow(w, w*RESOLUTION[1]/RESOLUTION[0])
		
		Window.reshape(self, w, w*RESOLUTION[1]/RESOLUTION[0])
	
