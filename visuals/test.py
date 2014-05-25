var = {
	"hue" : 0.0,
	"x" : 0.0,
}

PRE = 0

def loop():
	identity()
	linew(2)

	c = Color(0.5).hsv()
	c.set(0.05)

	cube = Cube()
	cube.x = x

	#for i in xrange(int(1e3)):
	#	cube.draw()
	#	cube.r *= 0.9

	#return
	#cube = Cube()
	cube.r = 2
	for i in xrange(15):
		for j in xrange(20):
			cube.draw()
			rotate(0.1, 0.2)
		cube.r *= 0.8 + 0.1*bass
