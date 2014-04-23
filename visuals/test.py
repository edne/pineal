def loop():
	identity()
	
	
	palette(GREY)
	linew(2)
	rotatex(1.2)
	rotate(time_rad())
	
	ambient(1)

		
	c = Cube()

	def step(i):
		translate(high*2,0)
		scale(0.5)
		rotate(time_rad())

	c.step = step
		
	c.r = 1.0 + bass*2
	c.fa = 0.2
	c.ni = 15
	c.draw()
	
	palette(HSV)
	identity()
	p = Polygon(4)
	p.fa = 0.5
	#p.draw()
	
