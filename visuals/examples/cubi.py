
var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():
	#identity()
	strokeWeight(1)

	r = rad


	rotateX(dt)
	rotateY(dt*0.5)

	colorMode("hsv")
	c = Color(note+0.5, alpha/2)
	fill(c)
	#noFill()

	colorMode("rgb")
	stroke(0, alpha)

	#for i in xrange(200):
	#	octahedron(r)
	#	r *= 0.9

	for x in np.arange(-0.7, 0.7,0.2):
		for y in np.arange(-0.7,0.7,0.2):
			for z in np.arange(-0.7,0.5,0.2):
				pushMatrix()
				translate(x*2,y*2,z*2)
				cube(0.08)
				popMatrix()
