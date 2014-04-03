def loop():
	palette(HSV)
	
	p = Polygon(6)
	#p = Icosahedron()
	#p=Cube()
	
	p.fa = 0.2
	p.h = note+0.3
	#p.h = 0.5 + note/2
	
	linew(2)
	
	p.h = note+0.3
	p.fa = 0.2
	p.h = note+0.3
	for i in xrange(9):
		push()
		#p.x = -1 + 2*i*1.0/9
		translate(-1 + 2*i*1.0/9, 0)
		p.h += amp/9
		p.r = band[i]
		p.draw()
		pop()
	p.x = 0
	
	
	

class Ring(Centered):
	def __init__(self, shape, n, x=0, y=0, r=1, ang=0):
		Centered.__init__(self, x,y,r)
		self.ang = ang
		self.shape = shape
		self.n = n
	
	def draw(self):
		push()
		
		rotate(self.ang)
		
		for i in xrange(self.n):
			push()
			translate(self.r, 0)
			self.shape.draw()
			pop()
			rotate(2*pi/self.n)
		
		pop()

class Nestled(Centered):
	def __init__(self, shape, n, ratio=0.5, x=0, y=0, r=1, ang=0):
		Centered.__init__(self, x,y,r)
		self.ang = ang
		self.shape = shape
		self.n = n
		self.ratio = ratio
	
	def draw(self):
		push()
		
		rotate(self.ang)
		scale(self.r)
		
		h = self.shape.h
		self.shape.h += self.h
		
		for i in xrange(self.n):
			push()
			#translate(self.r, 0)
			self.shape.draw()
			pop()
			#rotate(2*pi/self.n)
			rotate(0.1)
			scale(self.ratio)
		
		self.shape.h = h
		
		pop()

