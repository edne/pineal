def loop():
	None

def _loop():
	#identity()
	
	#poligoni1()
	#ciclo1()
	
	#ciclo2()
	#ciclo3()
	
	#logo()
	
	identity()
	
	palette(GREY)
	
	p = Polygon(4)
	p.r = amp
	#p.draw()
	
	#ciclo_base()
	#ciclo_annidato()
	#ricorsione_base(8)
	#immagine_meno_bassi()
	
	
	palette(HSV[:2])
	#raggi1()
	
	#palette([cG,cY,cC])
	#rec1(5)
	
	#a = 10
	#mem(a, "lettera")
	#clear("lettera")

def immagine_meno_bassi():
	t = Image('alquemix_mask')
	
	#t.h = note
	#t.a = 0.5-bass*2
	t.draw()

def ciclo_base():
	p = Polygon(4)
	p.fa = 0.5
	p.r = 0.5*bass
	p.x = 0.5+high
	
	p.ang = time_rad(-2)
	
	n = 8
	push()
	rotate(time_rad())
	for i in xrange(n):
		p.draw()
		rotate(2*pi/n)
	pop()

def ciclo_annidato():
	#p = Polygon(4)
	p = Tetrahedron()
	p.fa = 0.1
	
	
	p.ang = time_rad(-2)
	
	n = 9
	m = 6
	push()
	rotate(time_rad())
	for i in xrange(n):
		
		for j in xrange(m):
			
			p.r = bass*0.1*(j+1)
			p.x = bass*0.2*(j+1)
			
			rotatex(2*pi/m)
			p.draw()
		
		rotate(2*pi/n)
	pop()

def ricorsione_base(rec=1):
	push()
	
	p = Polygon(4)
	p.fa = 0.1
	
	p.draw()
	
	scale(0.5)
	rotate(time_rad())
	if rec>1:
		ricorsione_base(rec-1)
	pop()


def rec1(rec=1):
	push()
	#p = Polygon(4)
	p = Tetrahedron()
	
	p.fa = amp*rec/8
	p.r = amp*4/rec
	
	p.h = note+0.1*rec
	
	p.draw()
	
	
	
	rotatey(time_rad(0.5))
	rotatex(time_rad()+high)
	if rec>1:
		rec1(rec-1)
	
	pop()
	
def logo():
	push()
	
	identity()
	palette(GREY)
	t = Image('alquemix_mask')
	#t = Polygon(4)
	
	t.a = amp+0.1
	t.r = bass*2
	
	rotatey(amp*(time%(2*pi)))
	
	t.draw()
	pop()

def raggi1():
	#p = Polygon(4)
	#p = Polygon(20)
	#p = Circle()
	
	p = Tetrahedron()
	
	p.fa = high
	
	push()
	
	nr = 7
	n = int(8 + 16*bass)
	rotatex(-1 + bass*2)
	for i in xrange(nr):
		p.x = bass
		p.r = bass/2
		p.h = note
		
		push()
		for j in xrange(n):
			#rotatey(4*high*2*pi)
			p.draw()
			p.r *= 1.1 + bass*2
			p.x += p.r + amp/2
			p.h += 1.0/n
			rotate(2*2*pi/nr)
			rotate(time_rad(-0.1))
		pop()
		rotate(2*pi/nr)
	
	pop()

def poligoni1():
	push()
	palette(GREY)
	p = Icosahedron()
	
	rotatey(time%(2*pi))
	rotatex(high*2 + 2*time%(2*pi))
	
	n = 5
	for i in xrange(1,n+1):
		p.r = 2*bass/i
		p.fa = 0.05
		p.sa = bass
		
		#rotatex(bass)
		#rotatey(0.2*amp)
		
		push()
		rotate(time_rad(4))
		p.draw()
		pop()
	
	pop()


def ciclo1():
	palette(GREY)
	
	p = Polygon(4)
	
	p.fa = 0.1
	p.r = high
	
	push()
	
	rotate(time%(2*pi) + high*5)
	
	n = 10
	for i in xrange(n):
		p.x = bass*2
		rotate(2*pi/n)
		p.draw()
	pop()


def ciclo2():
	palette(HSV[3:])
	
	p = Polygon(4)
	
	p.fa = 0.1
	p.sa = amp*2
	p.r = high
	
	p.h = note
	
	push()
	
	rotate(-time%(2*pi) + high*5)
	
	n = 10
	for i in xrange(n):
		p.x = amp
		rotate(2*pi/n)
		p.draw()
	pop()

def ciclo3():
	palette(HSV)
	
	push()
	
	rotatex(time%(2*pi))
	scale(3)
	palette(HSV[:3])
	
	#p = Polygon(4)
	p = Tetrahedron()
	
	linew(2)
	
	p.fa = amp/4
	p.sa = 0.1
	p.r = high
	
	p.h = note
	
	push()
	
	rotate(-time%(2*pi) + high*5)
	
	n = 10
	for i in xrange(n):
		p.x = amp
		rotate(2*pi/n)
		p.draw()
	pop()
	
	pop()
