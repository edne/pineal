def loop():
	memory_example()
	None

def memory_example():
	p = Polygon(4)
	
	
	p = mem(p,"pol")
	
	p.r += dt
	if p.r > 1:
		p.r = 0
	
	p.draw()
	#clear("pol")

def prove8():
	identity()
	#prove4_edited()
	#prove6()
	#prove8()
	
	palette(HSV)
	p = Icosahedron()
	linew(2)
	p.sa = 0.1
	
	rotatey(0.5*time%(2*pi))
	for i in xrange(1,6):
		p.r = (bass*1.0)/(i-high*2)
		p.fa = 0.1
		p.h = 0.5*(time%(2*pi)) + 0.05*i + 0.3
		#p.draw()
		rotatex(0.5*time%(2*pi))
		rotatey(0.5*time%(2*pi))
			
	
	identity()
	rec_sq(4)
	
	
	identity()
	palette(GREY)
	#t = Image('xqz_mask')
	t = Polygon(4)
	
	t.a = bass
	
	t.h = p.h
	t.y = 0.03*high
	t.x = 0.05*high
	#t.r = 0.8 + 0.2*bass
	t.r = 0.8 + 0.2*bass
	t.h = 0
	t.draw()
	
	t.y = 0
	t.x = 0
	t.r = 0.8 + 0.2*bass + high/2
	
	
	palette(HSV)
	t.h = note/4+0.5
	
	t.draw()

def rec_sq(rec=1):
	
	palette(GREY)
	rotate(0.5*time%(2*pi) + high)
	#p = Polygon(3)
	p = Tetrahedron()
	translate(0.5*high,0)
	p.h = note/4+0.3
	
	p.fa = bass/4
	p.sa = high
	
	p.r = (bass)*rec*rec/8
	p.draw()

	rotate(0.5)
	rotatey(0.5*time%(2*pi))
	if rec>1:
		rec_sq(rec-1)

def prove8():
	push()
	
	p = Tetrahedron()
	#p = Teapot()
	p.fa = 0.1
	
	linew(2)
	
	n = 5
	for i in xrange(n):
		rotate(2*pi/n)
		
		push()
		
		p.r = bass + high
		
		
		rotatex(time%(pi*2))
		rotatey(time%(pi))
		
		palette(HSV)
		p.h = note
		
		for j in xrange(8):
			
			p.sa = 0.5*j
						
			p.x = (high*j - bass*4)
			p.draw()
			rotate(0.2+high)
			
			
			p.h += 0.05
		p.draw()
		
		
		pop()
	
	pop()

def prove4_edited():
	push()
	
	#rotatex(time%(2*pi))
	#rotatex(0.2*time%(2*pi)+bass)
	#rotatex(4*bass)
	
	n = 16
	#p = Polygon(4)
	p = Tetrahedron()
	
	
	rotatex(-bass)
	
	#translate(-pi,0)
	for i in xrange(n):
		rotate(2*pi/n)
		#translate(2*pi/n,0)
		push()
		
		linew(2)
		p.fa = amp
		p.sa = 1
		
		p.h = note
		p.r = bass + 0.1*noise()*high
		#p.x = 3*bass + 2*high*noise()
		p.x = amp
		
		rotate(0.2*time%(2*pi)+bass)
		#rotate(time%(2*pi))
		
		linew(1.5)
		palette(HSV[3:5])
		#p.a = note+high
		p.a = amp+bass
		p.draw()
		
		#rotatey(time%(2*pi))
		
		#p = Polygon(3)
		linew(2)
		p.h = 0.21+high*4
		p.sa = 1
		p.fa = bass
		p.x *= 2.05+bass
		p.r += 2*high
		p.draw()
		
		
		p.a = 1
		p.sa = 1
		
		rotatey(bass*10)
		
		
		palette(HSV[1:3])
		p.h = note
		p.x *= 1.5
		p.r *= high*4
		p.draw()
		
		#rotatey(-bass*30)
		#rotatex(-bass*30)
		
		p.h = note
		p.x *= 0.5
		p.r *= high*3
		p.draw()
		
		palette(GREY)
		p.h = note+0.3
		p.x *= 0.5
		p.r *= high*2
		p.draw()
		
		pop()
	
	pop()

def prove7():
	#part1()
	
	
	part2()

def part1():
	n = 3
	
	p = Polygon(4)
	#p = Sphere()
	p.fa = 0.2*amp
	p.sa = 0.5
	
	
	
	p.a = 0.2
	p.sa = 2*amp
	n = 7
	for i in xrange(10):
		p.h = i*0.01 + note+0.1*i/n
		for j in xrange(n):
			p.r = 0.5*amp + bass
			p.x = bass + 1.0*i/10
			
			push()
			rotatey(pi*(1-bass))
			#p.draw()
			pop()
			
			rotate(2*pi/n)
		p.fa = 0.1*amp*(10-i)
		rotate(bass*2*pi/10)
	
	
	rotate(time%(2*pi))
	rotatex(time%(2*pi))

def part2():
	
	#p = Polygon(4)
	p = Tetrahedron()
	p.sa = amp
	
	p.a = 1
	p.fa = amp/2+high
	n = 4
	for i in xrange(n):
		p.h = 0.5+note+0.2*i/n
		rotatex(i*2*pi/n)
		push()
		for j in xrange(n):
			push()
			rotatex(bass)
			rotatex(i*2*pi/n)
			translate(bass, 0.2, 0)
			scalexyz(bass*i/10, 0.2+high, 1)
			p.draw()
			pop()
			rotate(10*amp+2*pi/n)
			
		pop()
		rotate(high+2*pi/n)

def prove6():
	identity()
	
	rec_cube(2)
	
	n = 3
	for i in xrange(n):
		
		rotate(2*pi/n)
		push()
		
		
		translate(bass*2,0)
		prove5(HSV)
		
		prove5(GREY)
		
		pop()
	
	#rec_cube(2)

def prove5(pal=HSV):
	palette(pal)
	
	#p = Polygon(3)
	p = Tetrahedron()
	
	p.a = 0.6
	p.h = 0.2+note*0.5
	#p.a = 2*bass
	p.fa = 0.5*amp
	p.sa = 1*amp*5
	p.r = 2*bass
	
	n = 3
	
	rotatex(amp*2+0.2*time%(2*pi))
	
	for i in xrange(n):
		p.draw()
		
		p.r -= bass
		rotate(amp+bass)
		
		rotatey(high+time%(2*pi))
		
		translate(0,0,bass)

def rec_cube(i=1):
	rotatex(0.5*time%(2*pi)+bass)
	
	push()
	
	linew(2)
	
	palette(HSV)
	#c = Polygon(4)
	c = Tetrahedron()
	
	rotate(0.3)
	rotatey(0.1)
	
	
	c.h = 0.1*(i*i)+note + 0.2*time%(2*pi)
	
	
	c.a = 2*amp
	c.fa = 0.05
	c.sa = 1
	c.r = 0.5/(i*2+high) + bass
	c.draw()
	
	rotatey((time/10)%(2*pi))
	
	if i>1:
		#rec_cube(i-(0.2+high))
		rec_cube(i-0.3)
	
	pop()

def recursive(rec=1):
	push()
	palette(HSV[2:])
	p = Polygon(6)
	p.h = note+0.1*rec
	p.sa = amp+5*high
	p.fa = 0.2*amp
	p.r = bass*(amp*rec+bass + noise()*high)
	
	
	rotatey(time%(2*pi)+bass)
	p.draw()
	
	p.r = bass
	rotate(1)
	rotatey(time%(0.2*pi)+bass)
	p.draw()
	
	
	translate(amp/2,0)
	if rec>1:
		recursive(rec-1)
	
	pop()

def prove4():
	push()
	
	#rotatex(time%(2*pi))
	rotatex(0.2*time%(2*pi)+bass)
	#rotatex(4*bass)
	
	n = 16
	p = Polygon(4)
	
	
	rotatex(-bass)
	
	#translate(-pi,0)
	for i in xrange(n):
		rotate(2*pi/n)
		#translate(2*pi/n,0)
		push()
		
		linew(2)
		p.fa = amp
		p.sa = 1
		
		p.h = note
		p.r = bass + 0.1*noise()*high
		#p.x = 3*bass + 2*high*noise()
		p.x = amp
		
		rotate(0.2*time%(2*pi)+bass)
		#rotate(time%(2*pi))
		
		linew(1.5)
		palette(HSV[2:4])
		#p.a = note+high
		p.a = amp+bass
		p.draw()
		
		rotatey(time%(2*pi))
		
		#p = Polygon(3)
		linew(2)
		p.h = 0.21+high*4
		p.sa = 1
		p.fa = bass
		p.x *= 2.05+bass
		p.r += 2*high
		p.draw()
		
		
		p.a = 1
		p.sa = 1
		
		rotatey(bass*10)
		
		
		palette(HSV[:2])
		p.h = note
		p.x *= 1.5
		p.r *= high*4
		p.draw()
		
		rotatey(-bass*30)
		rotatex(-bass*30)
		
		p.h = note
		p.x *= 0.5
		p.r *= high*3
		p.draw()
		
		palette(GREY)
		p.h = note+0.3
		p.x *= 0.5
		p.r *= high*2
		p.draw()
		
		pop()
	
	pop()

def prove1():
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

def prove2():
	
	palette(HSV[:2])
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
		
	

def prove3():
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
