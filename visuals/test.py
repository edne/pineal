var = {
	"hue" : 0.0
}

def loop():
	identity()

	p = Polygon(3)

	rotate(time_rad())

	p.fa = 0.1
	p.ni = 2
	p.draw()
