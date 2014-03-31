def loop():
	palette(GREY)
	
	p = Polygon(4)
	p.h = note
	
	p.r = 2*bass + 2*high*random(0,1)
	p.draw()
	
