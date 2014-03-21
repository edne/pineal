from imports import *
from visuals import *
from loader import *
from server import *

class MainClass:
	def __init__(self):
		
		glutInit(sys.argv)
		
		glutInitWindowSize(RESOLUTION[0], RESOLUTION[1])
		glutCreateWindow(TITLE)
		glutDisplayFunc(self.update)
		glutReshapeFunc(self.reshape)
		
		
		#glutInitWindowSize(RESOLUTION[0]/2, RESOLUTION[1]/2)
		#glutCreateWindow('Overview')
		#glutDisplayFunc(self.update)
		#glutReshapeFunc(self.reshape)
		
		glutSetCursor(GLUT_CURSOR_NONE)
		
		#glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glEnable( GL_LINE_SMOOTH )
		glEnable( GL_POLYGON_SMOOTH )
		#glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )
		#glHint( GL_POLYGON_SMOOTH_HINT, GL_NICEST )
		glHint( GL_LINE_SMOOTH_HINT, GL_FASTEST )
		glHint( GL_POLYGON_SMOOTH_HINT, GL_FASTEST )
		
		glEnable( GL_VERTEX_ARRAY )
		
		self.lastTime = glutGet(GLUT_ELAPSED_TIME);
		
		self.visuals = Visuals(self)
		self.server = Server(self)
		self.loader = Loader(self)
		
		self.loader.start()
		self.server.start()
		
		if DEVILSPIE:
			self.devilspie = subprocess.Popen("devilspie")
		
	def run(self):
		try:
			glutMainLoop()
			#while True:
			#	self.update()
			#	# glut main iteration??
		except KeyboardInterrupt:
			None
		
		print
		self.loader.stop()
		self.server.stop()
		
		if DEVILSPIE:
			self.devilspie.kill()
	
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
		
		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT)
		
		self.visuals.update()
		
		glFlush()
	
	def reshape(self, w,h):
		
		# sembra essere necessaria per il KeyboardInterrupt e stampa FPS
		#glutReshapeWindow( RESOLUTION[0], RESOLUTION[1])
		glutReshapeWindow( w,h )
		# problema di timing...
		
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
		None
	

