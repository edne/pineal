var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():
	colorMode("hsv")
	fill(note(),1,1,0.05)
	stroke(0.2, 0.1)
	strokeWeight(2)

	#return
	r = 2.5*amp()*10
	for i in xrange(100):
		cube(r)
		r *= 0.9
