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
		rotatey(time_rad())
	
	t = Teapot()
	t.r = 0.5
	t.fa = 1
	t.sa = 0
	
	t.x = 0
	
	t.transform = rot
	#t.transform = lambda: rotatex(time_rad())
	
	
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
	#glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
	glLightfv(GL_LIGHT0, GL_POSITION,[0.0, 3.0, 3.0, 3.0])
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[0.2, 0.2, 0.2, 1.0])
	#glEnable(GL_LIGHTING)
	#glDisable(GL_LIGHTING)
	#glEnable(GL_LIGHT0)
	
	
	glMaterialfv(GL_FRONT, GL_AMBIENT,[0.7, 0.7, 0.8, 0.0])
	#glMaterialfv(GL_FRONT, GL_DIFFUSE,[0.1, 0.0, 0.6, 0.0])
	glMaterialfv(GL_FRONT, GL_SPECULAR,[0.7, 0.6, 0.8, 0.0])
	glMaterialf(GL_FRONT, GL_SHININESS, 80)
	
	#t.draw()
	pop()
	
	identity()
	
	p = Polygon(4)
	
	
	p.transform = lambda: rotatex(bass*8+0.5)
	
	p.r = 0.5 + bass*8
	
	p.fa = 0.2*amp+0.1
	p.ni = 8
	
	def step(i):
		rot()
		scale(0.5)
		#rotate(2*pi/p.ni)
		translate(4*high*noise(), 0, amp*2+0.2)
	p.step = step
	
	#rot()
	
	p.draw()
	p.step = step
	
	ri = Ring(p, 4)
	ri.r = bass+0.5
	ri.draw()
	
