var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():
	#identity()
	strokeWeight(2)

	rotateX(dt*2)
	rotateY(dt*4)

	colorMode("hsv")
	c = Color(sin(time)*0.5+0.5, 0.1*alpha)
	fill(c)

	colorMode("rgb")
	stroke(c.h, alpha)

	cube = Cube()

	for i in xrange(12):
		cube.draw()
		cube.r *= 0.8
