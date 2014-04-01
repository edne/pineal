def loop():
	palette(GREY)
	
	p = Polygon(4)
	p.h = 0.5 + note/2
	
	p.r = 0.1 + 2*bass + 2*high*random(0,1)
	p.draw()
	
