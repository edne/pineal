var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():

	rotateY(dt/2)

	colorMode("hsv")

	h = note()
	fill(h,1,1,amp()*0.1)
	#noStroke()
	stroke(h+0.3,1,1,amp())
	strokeWeight(4)

	f = fill(); s = stroke()
	glColor4f(f.r,f.g,f.b, f.a)

	pushMatrix()
	rotateX(pi/2)
	l = bass()*10 + 2
	for i in xrange(100):
		quad(l)
		l *= 0.9
		rotateY(bass()*0.1+pi/4)
		rotateX(bass()*0.1+pi/4)
	popMatrix()
