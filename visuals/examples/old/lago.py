def loop():
	
	palette(GREY)
	
	p = Cube()
	p.fa = band[2]
	p.r = band[4]+high
	
	push()
	rotatex(time_rad()+high)
	rotatey(time_rad())
	
	for i in xrange(len(band)):
		p.fa = band[i]/9 + 0.1/(i+1)
		p.r = band[i]*i*4
		
		palette(GREY)
		p.h = 0.5
		#p.draw()
		
		palette(HSV)
		p.h = note
		#p.draw()
	pop()
