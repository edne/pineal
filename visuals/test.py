var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():

	colorMode("hsv")
	fill(0,0,0,0.1)
	stroke(0.5)
	strokeWeight(2)

	r = 1.0
	for i in xrange(100):
		cube(r)
		r *= 0.9
