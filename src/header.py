from src.imports import *
from math import *
from random import uniform

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

_palette = HSV

def palette(p):
	global _palette
	_palette = p

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
	def __init__(self, x=0, y=0, h=0, a=1):
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

class Triangle(Shape):
	def __init__(self, x=0, y=0, l=1, m=0.6, h=0.25, a=1):
		Shape.__init__(self, x,y, h,a)
		self.l = l
		self.m = m
		self.h = h
	
	def draw(self, dx=0, dy=0, da=1, dh=0):
		vertex = np.matrix(
			[
				[self.x+dx, self.y+dy],
				[self.x+dx + self.l, self.y+dy],
				[self.x+dx + self.m, self.y+dy + self.h]
			]
		)
		glVertexPointerd( vertex )
		
		set_color(self.h+self.fh+dh, self.a*self.fa*da)
		glDrawArrays( GL_POLYGON, 0, len(vertex) )
		
		set_color(self.h+self.sh+dh, self.a*self.sa*da)
		glDrawArrays( GL_LINE_LOOP, 0, len(vertex) )
	
	def vertex(self):
		return [
				[self.x, self.y],
				[self.x + self.l, self.y],
				[self.x + self.m, self.y + self.h]
			]

class Centered(Shape):
	def __init__(self, x=0, y=0, r=1, h=0, a=1):
		Shape.__init__(self, x,y, h,a)
		self.r = r

class Polygon(Centered):
	def __init__(self, n, x=0, y=0, r=1, ang=0, h=0, a=1):
		Centered.__init__(self, x,y,r, h,a)
		self.n = n
		self.ang = ang
	
	def draw(self, dx=0, dy=0, da=1, dh=0):
		vx = self.r*np.cos(self.ang+np.linspace(0,2*pi, self.n+1)) + self.x+dx
		vy = self.r*np.sin(self.ang+np.linspace(0,2*pi, self.n+1)) + self.y+dy
		vertex = np.column_stack((vx,vy))
		
		glVertexPointerd( vertex )
		
		set_color(self.h+self.fh+dh, self.a*self.fa*da)
		glDrawArrays( GL_POLYGON, 0, len(vertex) )
		
		set_color(self.h+self.sh+dh, self.a*self.sa*da)
		glDrawArrays( GL_LINE_LOOP, 0, len(vertex) )
		
	
	def vertex(self):
		vx = self.r*np.cos(self.ang+np.linspace(0,2*pi, self.n+1)) + self.x
		vy = self.r*np.sin(self.ang+np.linspace(0,2*pi, self.n+1)) + self.y
		#return np.column_stack((vx,vy))[:-1]
		return np.column_stack((vx,vy))

class Circle(Polygon):
	def __init__(self, x=0, y=0, r=1, h=0, a=1):
		Polygon.__init__(self, 50, x,y,r, h,a)
	
	def vertex(self):
		return [[self.x, self.y]]

class Group(Shape, list):
	def __init__(self, l=list(), x=0, y=0, h=0, a=1):
		Shape.__init__(self, x,y, h,a)
		list.__init__(self)
		
		for s in l:
			self.append(s)
	
	def add(self, s):
		self.append(s)
	
	def draw(self, dx=0, dy=0):
		for s in self:
			s.draw(self.x+dx, self.y+dy)
	
	def vertex(self):
		l = Shape.vertex(self)
		
		for s in self:
			vs = s.vertex()
			for v in vs:
				l.append(v)
		
		return l

def rotate(angle):
	#ctx.rotate(angle)
	glRotatef(180.0*angle/pi, 0,0, 1)

def translate(x,y):
	glTranslatef(x, y, 0)

def push():
	glPushMatrix()

def pop():
	glPopMatrix()


def random(a=0, b=1):
	return uniform(a,b)

def noise(a=1):
	return uniform(-a,a)
