def loop():
	#palette([cY,cR,cY])
	#palette([cC,cB,cBL])
	palette(HSV)
	
	#palette([cWH,cB,cBL])
	g = Group()
	
	push()
	translate(bass*0.4*sin(bass*10*time), 0)
	
	linew(1.5)
	
	n = 3
	h = 0.1
	
	p = Polygon(n)
	p.a = 0.5
	p.r = 0.1
	p.fa = 0.2
	p.h = h
	p.ang = time+high
	#p.draw()
	g.add(p)
	g.draw()
	r = 0.5+2*amp*2*bass

	for i in xrange(2):
		h += 0.2
		
		g_old = g
		g = Group()
		
		for (nx,ny) in g_old.vertex():
			p = Polygon(n)
			p.r = r + high
			p.x = nx
			p.y = ny
			p.fa = 0.3
			p.h = h
			p.ang = (time+high)*(i+2)
			g.add(p)
			#p.draw()
		
		#g.draw()
		r *= 0.5
	
	pop()
	
	push()
	#palette([cWH,cC,cG])
	#palette(HSV[:2])
	palette(HSV)
	c = Circle()
	c.a = 1
	c.fa = 0.01
	c.r = bass*2 + 0.5
	linew(3)
	c.h = note + 0.5
	
	c.r = bass*bass*8
	#c.draw()
	
	linew(3)
	for i in xrange(int(50*bass)):
		c.x = i*bass
		c.y = high*random(-1,1)*i/4
		c.r = c.r*0.5*high + bass*c.r*2
		#c.draw()
		rotate(pi)
		#c.draw()
	
	pop()
	
	push()
	linew(2)
	t = Triangle()
	t.fa = high
	n = 10
	rotate(time%(2*pi))
	
	
	t.x = amp/2
	t.l = 2*bass
	t.m = note*t.l
	t.h = bass
	
	palette(GREY)
	for i in xrange(n):
		rotate(2*pi/n)
		
		t.draw()
		
		for (cx,cy) in t.vertex():
			p = Polygon(4, cx,cy, high)
			p.fa = 0.1
			
			p.h = note
			palette(HSV)
			#p.draw()
	
	
	t.x = amp/2
	t.l = 2*bass+0.5
	t.m = note*t.l
	t.h = bass+0.5
	t.sa = 0.5
	for i in xrange(n*2):
		rotate(2*pi/n)
		
		palette(GREY)
		
		t.l *= 0.8
		t.m *= 0.8
		t.x = high*i + bass
		#t.draw()
		
		for (cx,cy) in t.vertex():
			p = Polygon(3, cx,cy, high)
			p.fa = 0.1
			p.sa = 0
			
			p.h = note
			palette(HSV)
			#p.draw()
	pop()
	
	push()
	palette(GREY)
	
	p = Polygon(8)
	p.r = bass*2
	p.h = 0.5
	p.fa = 0.5
	#p.draw()
	
	p.r += bass*2
	for (x,y) in p.vertex():
		palette(GREY)
		a = Polygon(4, x,y, high)
		a.h = 0.5
		a.fa = 0.5
		#a.draw()
		
		#rotate(time%(2*pi))
		palette(HSV)
		a.r *= amp+bass
		a.h = note
		#a.draw()
	
	palette(GREY)
	p.a = 1
	p.fa = 1
	p.h = 0
	p.r -= bass*4
	p.n = 8
	#p.draw()
	
	pop()

def __loop():
	
	palette(HSV)
	p = Polygon(4)
	p.a = 1
	p.h = note
	p.r = bass+high
	p.draw()
	
	rotate(time)
	
	p = Polygon(4)
	for i in xrange(50):
		rotate(2*pi/16)
		
		p.a = 0.1
		palette(GREY)
		p.h = note+0.5
		p.r = bass
		p.x = 5*bass
		p.draw()
		
	

def _loop():
	palette(GREY)
	
	
	c1 = Circle(x=0.2, r=0.1)
	c1.h = time
	c2 = Circle(x=-0.2, r=0.1)
	c2.h = time + 0.33
	g = Group((c1,c2))
	
	rotate(time)
	g.h = time/10
	g.a = 0.8
	#g.draw()
	
	
	c = Polygon(4)
	#c = Circle()	
	#c.draw()
	#
	bass = 0.4*sin(time*2)
	amp = 0.5
	high = 0.03+0.01*sin(time)
	#
	c.r = bass
	c.a=0.4
	
	c.h = time
	
	c.draw()
	
	rotate(-pi/2)
	
	#n = int(20*bass+1)
	n = 10 + int(10*bass)
	
	for r in xrange(1,n):
		n = 10+r
		rotate(time*(n-r)/100)
		
		palette(GREY)
		for i in xrange(0,n):
			rotate(2*pi/n)
			#c.r = bass*amp * r
			c.r = bass/2 * r
			c.a=0.3/r
			c.x = amp*r
			c.draw()
		c.h += 0.1
		
		palette(HSV)
		#palette([cY,cR,cY])
		for i in xrange(0,n):
			rotate(2*pi/n)
			c.r = amp/10 * r
			c.a = 1.8/r
			#c.h = note
			c.x = high*10*r
			c.draw()
