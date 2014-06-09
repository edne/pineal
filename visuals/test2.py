var = {
	"hue" : 0.0,
	"alpha" : 1.0,
	"vel" : 0.5,
}

PRE = 0

def loop():
	#identity()
	linew(2)


	#rotatey(time_rad(0.2))


	cube = Cube()
	cube.stroke(Color(0.0).hsv(), alpha)

	cube.draw()
