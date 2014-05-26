var = {
	"hue" : 0.0,
	"val" : 0.0,
}

PRE = 0

def loop():
	identity()
	linew(2)

	rotatey(time_rad())

	c = Color(0.5).hsv()
	#c.set(0.05)

	cube = Regular(4)

	cube.fill(Color(hue+ note*0.1).grey(), 2*high+0.1)
	cube.stroke(Color(note*0.4).hsv(), high+0.1)

	#for i in xrange(int(1e3)):
	#	cube.draw()
	#	cube.r *= 0.9

	#return
	#cube = Cube()
	cube.r = 1
	for i in xrange(25):
		for j in xrange(10):
			cube.draw()
			rotate(0.1, 0.2)
		cube.r *= 0.9
