var = {
	"hue" : 0.0,
}

PRE = 0

def loop():
	identity()
	linew(1)

	c = Color(0.5).hsv()
	c.set()

	p = Regular(8)
	p.r = 0.5 + high
	p.ni = 7

	p.stroke()
	p.draw()

	g = Grid(p, 3,3,1)
	g.r = bass*20 + 0.1
	g.draw()

	g = Grid(p, 3,3,1)
	g.r = bass*20 + 0.5
	g.draw()
