from pineal.graphic import *
from pineal.color import Color
from math import *
from random import uniform, gauss
import numpy as np

# epydoc --no-private --no-frames --parse-only src/header.py --output=doc

def time_rad(scale=1):
	""" scale time (in seconds) and mod by 2pi """
	return (time.time()*scale)%(2*pi)

def linew(w):
	""" line width """
	glLineWidth(w)

class Shape(object):
	"""
	generic shape
	@ivar x,y: position
	@ivar a: alpha
	@ivar fa: fill alpha
	@ivar sa: stroke alpha
	"""
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

		self.fill = Color()
		self.stroke = Color()
		self._h = 0

		self.a = 1
		self.sa = 1
		self.fa = 1

		self.r = 1
		self.ang = 0
		self.ni = 1  # number of iteration ;)

	def transform(self):
		"""called before drawing (shoud be overrided)"""
		None

	def before(self, i=0):
		"""called before each drawing iteration (shoud be overrided),
		by dafault call scale(0.5)"""
		None
	def after(self, i=0):
		"""called after each drawing iteration (shoud be overrided),
		by dafault call scale(0.5)"""
		scale(0.5)

	def _solid(self):
		None
	def _wire(self):
		None

	def draw(self):
		"""translate, rotate, scale and draw"""
		push()

		translate(self.x, self.y, self.z)
		rotate(self.ang)

		self.transform()
		scale(self.r)

		push()
		for i in xrange(self.ni):
			self.before(i)

			set_color(self.fill, self.a*self.fa)
			self._solid()

			set_color(self.stroke, self.a*self.sa)
			self._wire()

			self.after(i)

		pop()

		pop()

	@property
	def h(self):
		return self._h
	@h.setter
	def h(self, value):
		self._h = value
		self.fill(value)
		self.stroke(value)

class Ring(Shape):
	"""
	draw a shape on the vertexes of a regular polygon
	@ivar shape: the shape to draw
	@ivar n: number of vertexes
	"""
	def __init__(self, shape, n):
		self.shape = shape
		self.n = n
		Shape.__init__(self)

	def draw(self):
		push()

		rotate(self.ang - pi/2)

		push()
		for i in xrange(self.ni):
			self.before(i)
			for j in xrange(self.n):
				push()
				translate(self.r, 0)
				self.shape.draw()
				pop()
				rotate(2*pi/self.n)

			self.after(i)
		pop()

		pop()


class Polygon(Shape):
	"""
	draw a regular polygon
	@ivar n: number of vertexes
	"""
	def __init__(self, n):
		self.n = n

		vx = np.cos(np.linspace(0,2*pi, self.n+1))
		vy = np.sin(np.linspace(0,2*pi, self.n+1))
		self._vertex = np.column_stack((vx,vy))

		Shape.__init__(self)

	def draw(self):
		#glVertexPointerd( self._vertex )
		glVertexPointer( 2, GL_DOUBLE, 0, self._vertex.ctypes.data)
		Shape.draw(self)

	def _solid(self):
		glDrawArrays( GL_POLYGON, 0, len(self._vertex) )

	def _wire(self):
		glDrawArrays( GL_LINE_LOOP, 0, len(self._vertex) )

class Circle(Polygon):
	def __init__(self):
		Polygon.__init__(self, 30)

class Cube(Shape):
	def _solid(self): glutSolidCube(1)
	def _wire(self): glutWireCube(1)

class Sphere(Shape):
	def _solid(self): glutSolidSphere(1, 30, 30)
	def _wire(self): glutWireSphere(1, 30, 30)

class Tetrahedron(Shape):
	def _solid(self): glutSolidTetrahedron()
	def _wire(self): glutWireTetrahedron()

class Dodecahedron(Shape):
	def _solid(self): glutSolidDodecahedron()
	def _wire(self): glutWireDodecahedron()

class Octahedron(Shape):
	def _solid(self): glutSolidOctahedron()
	def _wire(self): glutWireOctahedron()

class Icosahedron(Shape):
	def _solid(self): glutSolidIcosahedron()
	def _wire(self): glutWireIcosahedron()

class Teapot(Shape):
	def _solid(self): glutSolidTeapot(1)
	def _wire(self): glutWireTeapot(1)


#class Image(Shape):
	#"""
	#draw a png image, must be saved as images/name.png
	#before the start of the program
	#@ivar name: the image name (without extension)
	#"""
	#def __init__(self, name):
		#self.name = name
		#Shape.__init__(self)

	#def draw(self):
		#glBindTexture(GL_TEXTURE_2D, textures[self.name])

		#glEnable(GL_TEXTURE_2D)

		#glEnableClientState(GL_VERTEX_ARRAY)
		#glEnableClientState(GL_TEXTURE_COORD_ARRAY)

		#vertex = np.array([[0,0],[0,1],[1,1],[1,0]],np.float)
		#glVertexPointer(2,GL_FLOAT,0,vertex)
		#glTexCoordPointer(2,GL_FLOAT,0,vertex)

		#push()

		#scale(2*self.r)
		#translate(-0.5+self.x,-0.5+self.y)
		#glVertexPointerd( vertex )

		#_set_color(self.h, self.a)
		#glDrawArrays( GL_POLYGON, 0, len(vertex) )

		#pop()

		#glDisable(GL_TEXTURE_2D)

def rotatex(angle):
	""" rotation about x axis """
	glRotatef(180.0*angle/pi, 1,0, 0)

def rotatey(angle):
	""" rotation about y axis """
	glRotatef(180.0*angle/pi, 0,1, 0)

def rotatez(angle):
	""" rotation about z axis """
	glRotatef(180.0*angle/pi, 0,0, 1)

def rotate(angz, angy=0, angx=0):
	""" rotation """
	rotatex(angx)
	rotatey(angy)
	rotatez(angz)

def translate(x,y, z=0):
	glTranslatef(x, y, z)

def scale(ratio):
	scalexyz(ratio, ratio, ratio)

def scalexyz(rx, ry, rz):
	glScalef(rx, ry, rz)

def push():
	""" push the actual state in the openGL matrix stack """
	glPushMatrix()
def pop():
	""" pop the actual state in the openGL matrix stack """
	glPopMatrix()

def identity():
	""" clear applied transformations """
	glLoadIdentity()

def random(a=0, b=1):
	""" uniform distribution """
	return uniform(a,b)

def noise(a=1):
	""" white noise (uniform distribution in [-a,+a]) """
	return uniform(-a,a)

# light
def ambient(amb):
	""" set ambiental light intensity """
	glLightModelfv(
			GL_LIGHT_MODEL_AMBIENT|GL_LIGHT_MODEL_TWO_SIDE,
			vec(amb,amb,amb, 1.0)
		)
def light(val):
	""" set light intensity """
	glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(val, val, val, 1.0))

def light_pos(x,y,z):
	""" set light position """
	glLightfv(GL_LIGHT0, GL_POSITION, vec(x,y,z, 3))
#
