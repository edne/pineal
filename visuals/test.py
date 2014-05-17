var = {
	"hue" : 0.0,
}

PRE = 0

def loop():
	identity()
	linew(1)

	#p = Regular(3)
	#p.r = 0.1
	p = Polygon((0,0),(4*bass + 0.5, 0),(0.5,amp+0.1))

	def after(i):
		rotate(time_rad(-0.1))
		scale(0.99)
	p.after = after

	rotate(time_rad())

	p.fa = 0.5
	p.ni = 10

	p.fill.hsv()
	p.stroke.black()
	p.h = hue + note/4

	p.draw()

	#g = Grid(p, 2,2,1)
	#g.r = 1
	#g.draw()
