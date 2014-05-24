var = {
	"hue" : 0.0,
}

PRE = 0

def loop():
	identity()
	linew(1)

	c = Regular(8)
	c.r = 0.5 + high

	c.stroke()
	c.draw()

	g = Grid(c, 3,3,1)
	g.r = bass*20 + 0.1
	g.draw()

	g = Grid(c, 3,3,1)
	g.r = bass*20 + 0.5
	g.draw()
