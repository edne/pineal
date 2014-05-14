var = {
	"hue" : 0.0
}

def loop():
	identity()

	p = Polygon(3)

	rotate(time_rad())

	p.fa = 0.5
	p.ni = 10

	p.fill.hsv()
	p.stroke.black()
	p.h = hue

	p.draw()
