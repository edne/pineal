def loop():
	identity()
	
	
	palette(GREY)
	linew(1.2)
	rotatex(1.2)
	rotate(time_rad())
	
	ambient(0.6)

		
	c = Cube()

	def step(i):
		translate(sin(time_rad()),0)
		scale(0.5)
		rotatex(time_rad())

	c.step = step
		
	c.r = 1.0 + bass*2
	c.fa = 0.2
	c.ni = 4
	#c.draw()
	
	r = Ring(c, 8)
	r.r = 4
	
	def step(i):
		#translate(high*2+0.25,0)
		scale(0.5)
		rotatex(time_rad(0.2))
		rotatey(time_rad(0.1))
	r.step = step
	
	r.ni = 6
	#c.r = 0.5
	r.draw()
	
