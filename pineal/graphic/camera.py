from imports import *
	
def update():
	global x,y,z, up
	x = r * math.sin(ang_x)
	y = r * math.sin(ang_y)
	z = r * math.cos(ang_x)*math.cos(ang_y)
	
	# up[0] = ...
	up[1] = math.cos(ang_y)
	# up[2] = ...

def reset():
	global x,y,x, r, up, ang_x,ang_y
	r = (4.0/3)/math.tan(45.0/2)  # use size!
	up = [0,1,0]
	
	ang_x = 0
	ang_y = 0
	update()

def rotate(dx, dy):
	global ang_x,ang_y
	ang_x -= float(dx)/100
	ang_y += float(dy)/100
	
	update()

reset()
