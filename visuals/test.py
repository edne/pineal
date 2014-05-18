var = {
	"hue" : 0.0,
}

PRE = 0

def loop():
	identity()
	linew(1)

	push()

	#p = Regular(3)
	#p.r = 0.1
	p = Polygon((0,0),(4*bass + 0.5, 0),(0.5,amp+0.1))

	def after(i):
		rotate(time_rad(-0.1))
		scale(0.99)
	p.after = after

	rotate(time_rad())

	pop()

	p.fa = 0.5
	p.ni = 10

	p.fill.hsv()
	p.stroke.black()
	p.h = hue + note/4

	#p.draw()

	c = Regular(8)
	c.r = 0.5 + high

	c.fill(1)
	c.a = amp + 0.1
	c.draw()

	g = Grid(c, 3,3,1)
	g.r = bass*20 + 0.1
	g.draw()

	c = Regular(4)
	c.r = high

	c.a = 1.0
	c.fill.hsv()
	c.h = hue + note/4

	g = Grid(c, 3,3,1)
	g.r = bass*20 + 0.1
	g.draw()
