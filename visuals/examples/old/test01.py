def loop():
	palette(GREY)
	
	p = Polygon(4)
	#p = Icosahedron()
	#p=Cube()
	
	p.fa = 0.2
	p.h = note+0.3
	#p.h = 0.5 + note/2
	
	linew(2)
	identity()
	
	p.y = 0.8
	
	p.h = note+0.3
	p.fa = 0.2
	p.h = note+0.3
	for i in xrange(9):
		push()
		#p.x = -1 + 2*i*1.0/9
		translate(-0.9 + 2*i*1.0/9, 0)
		#p.h += amp/9
		p.r = 0.1 + band[i]
		#p.draw()
		pop()
	p.x = 0
	
	push()
	
	def rot():
		rotatex(time_rad())
		rotatey(time_rad()+noise()*band[-1])
	
	t = Teapot()
	t.r = 0.5
	t.fa = 1
	t.sa = 0
	
	t.x = 0
	
	t.transform = rot
	
	#t.draw()
	pop()
	
	identity()
	rot()
	#rotatex(1)
	rotate(pi+bass*4)
	
	ambient(0.5)
	
	palette(HSV)
	p = Icosahedron()
	
	def step(i):
		#rot()
		#scale(0.9-0.1*bass*4)
		scale(0.9)
		p.h += 0.01*noise()
		
		rotate(amp)
		translate(cos(i)*band[0]*0.1,sin(i)*band[1]*0.1)
		rotatex(0.1)
	
	p.r = bass*10 + 2
	
	p.sa = 1
	p.fa = 0.1
	p.h = 0.1*time%1.0 + note
	p.step = step
	p.ni = 100
	
	p.draw()
	
	identity()
	p = Polygon(4)
	
	
	p.transform = lambda: rotatex(bass*8+0.5)
	
	p.r = 0.5 + bass*8
	
	p.fa = 0.2*amp+0.1
	p.ni = 8
	
	p.h = p.h = 0.1*time%1.0 + note + 0.3
	
	def step(i):
		rot()
		scale(0.5)
		#rotate(2*pi/p.ni)
		translate(4*high*noise(), 0, amp*2+0.2)
	p.step = step
	
	rot()
	
	palette(HSV)
	
	
	ambient(0.5)
	light(0.8)
	
	p.draw()
	p.step = step
	
	ri = Ring(p, 4)
	ri.r = bass+0.5
	ri.draw()
	
