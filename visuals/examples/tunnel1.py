var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():

	rotate(dt/2)

	colorMode("hsv")

	h = note()
	fill(h,1,1,amp()*0.05)
	#noStroke()

	colorMode("rgb")
	stroke(high()*5,amp())
	strokeWeight(2)

	f = fill(); s = stroke()
	glColor4f(f.r,f.g,f.b, f.a)

	colorMode("hsv")

	pushMatrix()
	#rotateX(pi/2)
	l = bass()*100 + 2
	for i in xrange(50):
		fill(h,1,1,amp()*0.01)
		quad(l)
		l *= 0.9
		rotate(bass()*0.2+pi/4)
		h += 0.01
	popMatrix()
