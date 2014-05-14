var = {
	"hue" : 0.0,
}

def loop():
	identity()
	linew(1)

	#p = Regular(3)
	p = Polygon((0,0),(2, 0),(0.5,0.2))

	def after(i):
		rotate(time_rad(0.1))
		scale(0.9)
	p.after = after

	rotate(time_rad())

	p.fa = 0.5
	p.ni = 50

	p.fill.hsv(0,1)
	p.stroke.black()
	p.h = hue

	p.draw()
