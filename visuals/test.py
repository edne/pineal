var = {
	"hue" : 0.0,
	"alpha" : 1.0,
	"vel" : 0.5,
}

PRE = 0

def loop():
	#identity()
	linew(2)

	rotatex(dt*vel*2)
	rotatey(dt*vel*4)

	#rotatey(time_rad(0.2))

	c = Color(0.5).hsv()

	cube = Cube()
	#cube = Tetrahedron()
	#cube = Sphere()
	#cube = Octahedron()

	cube.r += bass*4

	cube.fill(Color(note*0.1).grey(), alpha/6)
	cube.stroke(Color(hue+note*0.4 + 0.5).hsv(), alpha)

	for i in xrange(12):
		cube.draw()
		cube.r *= 0.8
