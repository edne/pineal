var = {
	"hue" : 0.0
}

def loop():
	identity()

	p = Polygon(3)

	rotate(time_rad())

	p.fa = 0.5
	p.ni = 10

	p.f.hsv()
	#p.f(0.5)
	p.f(sin(time_rad(0.5))*0.1)
	p.f = p.f - 0.1


	p.draw()
