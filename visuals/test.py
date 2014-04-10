def loop():
	identity()
	
	rotatex(1.2)
	rotate(time_rad())
	
	ambient(0.1 + 5*noise()*high)
	
	c = Cube()
	c.r = 0.2 + bass*4
	c.fa = 0.2
	c.ni = 10
	c.draw()
