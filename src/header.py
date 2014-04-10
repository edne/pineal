from src.imports import *
from math import *
from random import uniform, gauss

cR = (1,0,0)
cG = (0,1,0)
cB = (0,0,1)

cY = (1,1,0)
cC = (0,1,1)
cM = (1,0,1)

cBL = (0,0,0)
cWH = (1,1,1)

GREY = [cBL, cWH, cBL]
HSV = [cR, cY, cG, cC, cB, cM, cR]

#P3 = Polygon(3)
#P4 = Polygon(4)

_palette = GREY

def mem(var, name):
	if name in _mem:
		return _mem[name]
	else:
		_mem[name] = var
		return var

def clear(name):
	if name in _mem:
		_mem.pop(name)

def palette(p):
	global _palette
	_palette = p

def time_rad(scale=1):
	return (time*scale)%(2*pi)

def linew(w):
	glLineWidth(w)

def set_color(h,a):
	
	h = fmod(h,1)
	pos = h*(len(_palette)-1)
	
	index = int(floor(pos))
	
	pos = pos - floor(pos)
	#pos /= (len(_palette)-1)dh
	
	c1 = _palette[index]
	c2 = _palette[index+1]
	
	r = (1-pos)*c1[0] + pos*c2[0]
	g = (1-pos)*c1[1] + pos*c2[1]
	b = (1-pos)*c1[2] + pos*c2[2]
	glColor4f(r,g,b, a)
	

class Shape:
	def __init__(self, x=0, y=0, h=0.5, a=1):
		self.x = x
		self.y = y
		self.h = h
		self.a = a
		
		self.sa = 1
		self.sh = 0
		self.fa = 1
		self.fh = 0
	
	def vertex(self):
		return list()

class Centered(Shape):
	def __init__(self, x=0, y=0, r=1, ang=0):
		Shape.__init__(self, x,y)
		self.r = r
		self.ang = ang
		
		self.ni = 1  # number of iteration ;)
	
	def transform(self):
		None
	
	def step(self, i=0):
		scale(0.5)
	
	def solid(self):
		None
	def wire(self):
		None
	
	def draw(self):
		push()
		
		translate(self.x, self.y)
		rotate(self.ang)
		
		self.transform()
		scale(self.r)
		
		push()
		for i in xrange(self.ni):
			#glEnable(GL_LIGHTING)
			set_color(self.h+self.fh, self.a*self.fa)
			self.solid()
			
			#glDisable(GL_LIGHTING)
			set_color(self.h+self.sh, self.a*self.sa)
			self.wire()
			
			self.step(i)
		pop()
		
		pop()


class Ring(Centered):
	def __init__(self, shape, n, x=0, y=0, r=1, ang=0):
		Centered.__init__(self, x,y,r)
		self.ang = ang
		self.shape = shape
		self.n = n
	
	def draw(self):
		push()
		
		rotate(self.ang - pi/2)
		
		for i in xrange(self.n):
			push()
			translate(self.r, 0)
			self.shape.draw()
			pop()
			rotate(2*pi/self.n)
		
		pop()


class GlutPreset(Centered):
	None

class Cube(GlutPreset):
	def solid(self): glutSolidCube(1)
	def wire(self): glutWireCube(1)

class Sphere(GlutPreset):
	def solid(self): glutSolidSphere(1, 30, 30)
	def wire(self): glutWireSphere(1, 30, 30)

class Tetrahedron(GlutPreset):
	def solid(self): glutSolidTetrahedron()
	def wire(self): glutWireTetrahedron()

class Dodecahedron(GlutPreset):
	def solid(self): glutSolidDodecahedron()
	def wire(self): glutWireDodecahedron()

class Octahedron(GlutPreset):
	def solid(self): glutSolidOctahedron()
	def wire(self): glutWireOctahedron()

class Icosahedron(GlutPreset):
	def solid(self): glutSolidIcosahedron()
	def wire(self): glutWireIcosahedron()

class Teapot(GlutPreset):
	def solid(self): glutSolidTeapot(1)
	def wire(self): glutWireTeapot(1)


class Polygon(Centered):
	def __init__(self, n, x=0, y=0, r=1, ang=0):
		Centered.__init__(self, x,y,r, ang)
		self.n = n
		
		vx = np.cos(np.linspace(0,2*pi, self.n+1))
		vy = np.sin(np.linspace(0,2*pi, self.n+1))
		self._vertex = np.column_stack((vx,vy))
	
	def draw(self):
		glVertexPointerd( self._vertex )
		Centered.draw(self)
	
	def solid(self):
		glDrawArrays( GL_POLYGON, 0, len(self._vertex) )
	
	def wire(self):
		glDrawArrays( GL_LINE_LOOP, 0, len(self._vertex) )

class Circle(Polygon):
	def __init__(self, x=0, y=0, r=1):
		Polygon.__init__(self, 50, x,y,r)

class Image(Centered):
	def __init__(self, name, x=0, y=0, r=1, ang=0):
		Centered.__init__(self, x,y,r)
		self.name = name
	
	def draw(self):
		glBindTexture(GL_TEXTURE_2D, textures[self.name])
		
		glEnable(GL_TEXTURE_2D)
	
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		
		vertex = np.array([[0,0],[0,1],[1,1],[1,0]],np.float)
		glVertexPointer(2,GL_FLOAT,0,vertex)
		glTexCoordPointer(2,GL_FLOAT,0,vertex)
		
		push()
		
		scale(2*self.r)
		translate(-0.5+self.x,-0.5+self.y)
		glVertexPointerd( vertex )
		
		set_color(self.h, self.a)
		glDrawArrays( GL_POLYGON, 0, len(vertex) )
		
		pop()
		
		glDisable(GL_TEXTURE_2D)

def rotate(angle):
	glRotatef(180.0*angle/pi, 0,0, 1)

def rotatex(angle):
	glRotatef(180.0*angle/pi, 1,0, 0)

def rotatey(angle):
	glRotatef(180.0*angle/pi, 0,1, 0)

def translate(x,y, z=0):
	glTranslatef(x, y, z)

def scale(ratio):
	glScalef(ratio, ratio, ratio)

def scalexyz(rx, ry, rz):
	glScalef(rx, ry, rz)

def push(): glPushMatrix()
def pop(): glPopMatrix()

def identity():
	glMatrixMode (GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-1, 1, -1, 1, -1, 1)
	
	(w,h) = RESOLUTION	
	glScalef(
		float(min(w,h))/w,
		-float(min(w,h))/h,
		1
	)
	gluPerspective (60, 4.0/3.0, 1.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	

def random(a=0, b=1):
	return uniform(a,b)

def noise(a=1):
	return uniform(-a,a)

# light
def ambient(amb):
	glLightModelfv(
			GL_LIGHT_MODEL_AMBIENT|GL_LIGHT_MODEL_TWO_SIDE,
			[amb,amb,amb, 1.0]
		)
def light(val):
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [val, val, val, 1.0])

def light_pos(x,y,z):
	glLightfv(GL_LIGHT0, GL_POSITION,[x,y,z, 3])
#
