var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():
	#identity()
	strokeWeight(2)

	rotateX(dt*2*(0.2+amp))
	rotateY(dt*4*(0.2+amp))

	colorMode("hsv")
	c = Color(note, 1)
	fill(c)

	colorMode("rgb")
	stroke(high*16, 1)

	r = (1+bass*4)*rad
	for i in xrange(100):
		r -= (0.001*high*16)*rad
		#cube(r)
