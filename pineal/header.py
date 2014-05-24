from pineal.graphic import *
from pineal.color import Color
from math import *
from random import uniform, gauss
import numpy as np

from scipy import weave
import pineal.utils as utils

# epydoc --no-private --no-frames --parse-only src/header.py --output=doc

def time_rad(scale=1):
	""" scale time (in seconds) and mod by 2pi """
	return (time.time()*scale)%(2*pi)

def linew(w):
	""" line width """
	glLineWidth(w)

class Cube(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

		self.r = 1

		self._vertex = np.array( [
			[-1.0,-1.0,-1.0],
			[-1.0, 1.0,-1.0],
			[ 1.0, 1.0,-1.0],
			[ 1.0,-1.0,-1.0]
		] )
		glVertexPointer( 3, GL_DOUBLE, 0, self._vertex.ctypes.data)


	def draw(self):
		#glutWireCube(self.r)

		#vertex = utils.rotate(self._vertex, math.pi/2, np.array([0,1,0]))
		#a = 4
		#glDrawArrays( GL_POLYGON, 0, len(self._vertex) )
		#glDrawArrays( GL_LINE_LOOP, 0, 4 )

		r = self.r
		support = "#include <GL/freeglut.h>"
		code = """
			glutWireCube(r);

/*GLfloat		faces[] =
  {
    -1, -1, -1,   -1, -1,  1,   -1,  1,  1,   -1,  1, -1,
     1, -1, -1,    1, -1,  1,    1,  1,  1,    1,  1, -1,
    -1, -1, -1,   -1, -1,  1,    1, -1,  1,    1, -1, -1,
    -1,  1, -1,   -1,  1,  1,    1,  1,  1,    1,  1, -1,
    -1, -1, -1,   -1,  1, -1,    1,  1, -1,    1, -1, -1,
    -1, -1,  1,   -1,  1,  1,    1,  1,  1,    1, -1,  1
  };

glVertexPointer(3, GL_FLOAT, 0, faces);

int i;

for(i=0; i<24; i++)
	faces[i] *= r;

for(i=0; i<6; i++)
{
GLint indices[] = {0+(i*4),1+(i*4),2+(i*4),3+(i*4)};
glDrawElements( GL_LINE_LOOP, //mode
                4,  //count, ie. how many indices
                GL_UNSIGNED_INT, //type of the index array
                indices);
}
//glDrawArrays(GL_LINE_LOOP, 0, 4);
*/
		"""

		weave.inline(code, ['r'], support_code = support, libraries = ['GL','glut','GLU'])




class Shape(object):
	"""
	generic shape
	@ivar x,y: position
	"""
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

		self.r = 1
		self.ang = 0
		self.ni = 1  # number of iteration ;)

		self._fill = False
		self._stroke = True

	def fill(self):
		self._fill = True
		self._stroke = False
	def stroke(self):
		self._fill = False
		self._stroke = True

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

			if self._fill: self._solid()
			if self._stroke: self._wire()

			self.after(i)

		pop()

		pop()

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

class Grid(Shape):
	def __init__(self, shape, l=1,m=1,n=1):
		self.shape = shape
		self.l,self.m,self.n = l,m,n
		Shape.__init__(self)

	def draw(self):
		push()

		for iteration in xrange(self.ni):
			self.before(iteration)

			for i in xrange(self.l):
				for j in xrange(self.m):
					for k in xrange(self.n):
						push()
						translate(
							(i-float(self.l-1)/2)*float(self.r)/self.l,
							(j-float(self.m-1)/2)*float(self.r)/self.m,
							(k-float(self.n-1)/2)*float(self.r)/self.n,
						)
						self.shape.draw()
						pop()

			self.after(iteration)

		pop()


class Polygon(Shape):
	def __init__(self, *vertex):
		vertex = list(vertex)
		vertex.append(vertex[0])
		self._vertex = np.array(vertex)
		Shape.__init__(self)

	def draw(self):
		#glVertexPointerd( self._vertex )
		glVertexPointer( 2, GL_DOUBLE, 0, self._vertex.ctypes.data)
		Shape.draw(self)

	def _solid(self):
		glDrawArrays( GL_POLYGON, 0, len(self._vertex) )

	def _wire(self):
		glDrawArrays( GL_LINE_LOOP, 0, len(self._vertex) )

class Regular(Polygon):
	"""
	draw a regular polygon
	@ivar n: number of vertexes
	"""
	def __init__(self, n):
		self.n = n

		vx = np.cos(np.linspace(0,2*pi, self.n+1))[:-1]
		vy = np.sin(np.linspace(0,2*pi, self.n+1))[:-1]
		vertex = np.column_stack((vx,vy))

		Polygon.__init__(self, *vertex)

class Circle(Regular):
	def __init__(self):
		Regular.__init__(self, 30)

#class Cube(Shape):
#	def _solid(self): glutSolidCube(1)
#	def _wire(self): glutWireCube(1)

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

def translate(x,y=0, z=0):
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
