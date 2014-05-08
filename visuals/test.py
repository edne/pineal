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

	rotate(time_rad())
	
	#ambient(sum(band[6:])*noise())

		
	c = Cube()
	#c = Polygon(4)
	
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
	c.a = 1
	c.fa = sum(band[:2]) + 0.1
	c.ni = 3
	#c.draw()
	
	r = Ring(c, 8)
	r.r = (3 - sum(band[:2]))
	
	def before(i):
		#rotatex(time_rad(0.2))
		rotatey(time_rad(0.1) - bass)
		#c.h += 0.1
		#rotatey(time_rad(0.1))
		None
	r.before = before
	
	
	r.ni = 8
	#c.r = 0.5
	
	
	r.draw()
	
