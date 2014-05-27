var = {
	"hue" : 0.0,
	"ratio" : 0.5,
	"vel" : 0.5,
}

PRE = 0

def loop():
	identity()
	linew(2)

	#rotate(time_rad(vel))
	#rotatey(time_rad(0.2))

	c = Color(0.5).hsv()
	#c.set(0.05)

	cube = Cube()
	#cube = Tetrahedron()
	#cube = Sphere()
	#cube = Octahedron()

	cube.fill(Color(note*0.1).grey(), 2*high+0.0)
	cube.stroke(Color(hue+note*0.4).hsv(), high+0.1)

	#r = Ring(cube, 10)
	#r.draw()

	cube.r = 0.1 + ratio + bass


	for center in Ring(10, 1):
		cube.center = center
		cube.draw()
	cube.center = (0,0,0)

	#return


	#cube = Cube()
	cube.r = 2
	for i in xrange(25):
		for j in xrange(10):
			cube.draw()
			rotate(0.1, 0.2)
		cube.r *= ratio + bass
