def loop():
	
	rotatex(time_rad())
	rotatey(time_rad())
	
	linew(2)
	
	palette(HSV[2:5])
	#palette(HSV[1:5])
	c = Cube()
	sa = high*(sum(band[2:5]))+amp
	fa = sum(band[6:]) + band[0]
	r = 2*min(1.1,3*sum(band[2:5]))
	n = 20
	for i in xrange(n):
		c.sa = sa
		
		c.fa = log(i+1)*fa/(i+4)
		
		c.r = r/(i**1.5+1+bass)
	
		c.h = note + c.r
		
		#palette(HSV[2:5])
		
		rotatex(sum(band[2:5]))
		rotatey(sum(band[:2]))
		
		c.draw()
	
	
		
	linew(2)
	palette(GREY)
	raggio()
	rotate(pi/2)
	raggio()
	rotate(pi/2)
	raggio()
	rotate(pi/2)
	raggio()
	rotatey(pi/2)
	raggio()
	rotatey(pi)
	raggio()
	
	
	palette(GREY)
	c = Cube()
	
	linew(1)
	
	c.a = 0.5
	c.fa = 0.5
	c.r = 2*max(0, 0.2*amp - bass/2)
	#sigma = high*8
	sigma = band[-1]*16
	
	for i in xrange(100):
		push()
		c.h = noise(0.5)
		translate(gauss(0, sigma), gauss(0, sigma), gauss(0, sigma))
		
		#c.draw()
		pop()
	
	
def raggio():
	c = Cube()
	c.sa = high*(sum(band[2:5]))+amp*2
	c.fa = high + amp - bass/2
	
	x = 0
	for j in xrange(int(6*amp*10)):
		for i in xrange(6):
			
			c.r = 16*band[i]*2/(2*i+1)
			if c.x > 2: break
			if c.r > 1: continue
			push()
			translate(0, gauss(0, bass),gauss(0, bass))
			
			c.x = x + 10*band[4]+40*sum(band[:i])/(i+1)
			c.draw()
			
			pop()
		x = c.x
