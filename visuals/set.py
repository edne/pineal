def loop():
	identity()
	set1()
	None

def set1():
	palette(GREY)
	
	p = Polygon(4)
	
	
	p.r = bass*4
	p.fa = 1*high
	#p.draw()
	
	p = Polygon(4)
	p.fa = 1*high
	p.r = bass*6 + amp
	p.x = 0.2+bass
	
	p.ang = time_rad(-2)
	
	n = 9
	push()
	rotate(time_rad())
	for i in xrange(n):
		#p.draw()
		rotate(2*pi/n)
	pop()
	
	
	n = 9
	push()
	rotate(time_rad())
	for i in xrange(n):
		#p.draw()
		rotate(2*pi/n)
	pop()
	
	
	
	p = Polygon(4)
	p.fa = amp+high
	
	palette(HSV[2:5])
	n = 3
	p.r = bass
	p.x = 0.2+amp
	p.h = note
	push()
	rotate(time_rad())
	for i in xrange(n):
		#p.draw()
		rotate(2*pi/n)
	pop()
	
	
	ciclo_3()
	ciclo_1()
	ciclo_2()
	
	tetra(40)
	
	#immagine_meno_bassi()
	

def tetra(rec=1):
	linew(1.5)
	palette(HSV[:4])
	push()
	
	p = Tetrahedron()
	p.fa = 0.1
	p.sa = amp+bass*4
	
	p.h = 0.5 + note*rec/50
	
	p.r = bass*9+high
	
	rotatey(time_rad()+high*noise())
	
	p.draw()
	
	
	scale(0.8)
	if rec>1:
		tetra(rec-1)
	pop()


def ciclo_3():
	p = Polygon(3)
	#p = Tetrahedron()
	p.fa = 0.0 + 2*amp
	p.sa = 0.2+amp
	
	linew(2)
	palette(HSV)
	
	p.ang = time_rad(-2)
	
	n = 9
	m = 4
	push()
	#rotatex(0.2)
	#rotatey(time_rad(bass*4) + bass*4 + high*8)
	rotate(time_rad())
	for i in xrange(n):
		
		
		
		push()
		for j in xrange(m):
			p.h = note+0.5*bass
			
			p.r = 2*(bass*0.2*(j+1) + high*noise()*2)
			
			p.x = 0.1+(bass+0.1)*(j+1)
			p.x *= 0.8 + bass*4
			
			rotatex(2*pi/m)
			p.draw()
		pop()
		
		rotate(2*pi/n)
	pop()


def ciclo_1():
	
	#palette(HSV[2:5])
	palette(HSV)
	
	#p = Polygon(3)
	p = Tetrahedron()
	p.fa = 0.1+amp
	
	p.sa = 0.2+amp+bass
	
	p.h = note
	
	p.ang = time_rad(-2)
	
	linew(2)
	
	n = int(3*bass)
	m = 6
	push()
	
	#rotatex(time_rad(1.2))
	rotate(time_rad(1.2))
	for i in xrange(n):
		
		for j in xrange(m):
			
			p.r = 0.5*(0.1+bass)*(j+1)
			p.x = (0.1+bass+amp)*(j+1)
			
			rotatex(2*pi/m)
			#p.draw()
		
		rotate(2*pi/n)
	pop()

def ciclo_2():
	
	palette(GREY)
	
	p = Polygon(4)
	#p = Tetrahedron()
	p.fa = amp/2
	
	p.sa = amp*2+bass*1
	
	p.h = note+0.3
	
	#p.ang = time_rad(-2)
	
	linew(2)
	
	n = 9+int(bass*10)
	m = 6
	push()
	rotate(time_rad(1.5))
	#rotatex(time_rad(1))
	for i in xrange(n):
		
		for j in xrange(m):
			
			p.r = 0.7*bass*(j+1)
			p.x = (0.1+bass+amp)*(j+1)
			
			rotatex(2*pi/m)
			
			p.draw()
		
		rotate(2*pi/n)
	pop()


def immagine_meno_bassi():
	t = Image('alquemix_mask')
	
	palette(GREY)
	
	
	#t.h = note
	#t.a = 0.5 + bass
	t.a = 0.2  - bass
	t.r = amp*2+0.5
	t.h = 0.2
	t.draw()


def _prove():
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
	
	ciclo_base()
	#ciclo_annidato()
	#ricorsione_base(8)
	immagine_meno_bassi()
	
	
	palette(HSV[:2])
	#raggi1()
	
	#palette([cG,cY,cC])
	#rec1(5)
	
	#a = 10
	#mem(a, "lettera")
	#clear("lettera")

def trap():
	
	palette(HSV[:4])
	c = Circle()
	c.h = note
	
	c.x =  0.7+bass + high
	c.r = bass
	c.fa = 2*high
	
	linew(2)
	
	#c.draw()
	c.x = -c.x
	#c.draw()

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

