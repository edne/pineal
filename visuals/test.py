
var = {
	"alpha" : 1.0,
	"rad" : 1.0,
}

def loop():

	fill(0,0)
	stroke(1)
	strokeWeight(2)

	s = createShape()

	s.vertex(0,0)
	s.vertex(0,1)
	s.vertex(1,1)

	shape(s)
