var = {
	"variabile" : 0.5,
}

def loop():
	identity()
	
	
	#palette(GREY)
	palette(HSV)
	
	linew(1.2)
	rotatex(sum(band[:6]))
	#rotatex(1.2)

	#rotate(time_rad())
	
	#ambient(sum(band[6:])*noise())

		
	#c = Cube()
	c = Polygon(4)
	
	c.h = note
	
	def after(i):
		#translate(sin(time_rad()),0)
		translate(-sum(band[5:]),0)
		scale(0.5)
		#rotatex(time_rad())
		c.h += 0.002
		#

	c.after = after
		
	c.r = 1.0 + bass*2
	c.a = 0.5
	c.fa = sum(band[:2]) + 0.1
	c.ni = 3
	#c.draw()
	
	r = Ring(c, 8)
	r.r = (1 - sum(band[:2]))
	
	def before(i):
		#rotatex(time_rad(0.2))
		rotatey(-bass)
		#c.h += 0.1
		#rotatey(time_rad(0.1))
		#translate(0,0, 0.5*bass)
		None
	r.before = before
	
	
	r.ni = 5
	#c.r = 0.5
	
	
	r.draw()
	
