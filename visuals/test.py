def loop():
	palette(GREY)
	
	p = Polygon(4)
	p.fa = 0.5
	#p.h = 0.5 + note/2
	
	#p.r = 0.1 + 4*bass + 4*high*random(0,1)
	#p.draw()
	
	for i in xrange(9):
		p.x = -1 + 2*i*1.0/9
		p.r = band[i]
		p.draw()
	
