from imports import *

def calculate():
	global x,y,z, up
	x = r * math.sin(ang[0])
	y = r * math.sin(ang[1])
	z = r * math.cos(ang[0])*math.cos(ang[1])

	# up[0] = ...
	up[1] = math.cos(ang[1])
	# up[2] = ...

def reset():
	global x,y,x, r, up, ang, direction
	r = (4.0/3)/math.tan(45.0/2)  # use size!

	up = [0,1,0]
	ang = [0,0]

	direction = [0,0,0]

	calculate()

def rotate(dx, dy):
	global ang
	ang[0] -= float(dx)
	ang[1] += float(dy)

	calculate()

def start_rotate(dir_x, dir_y):
	global direction
	direction[0] += dir_x
	direction[1] += dir_y

def stop_rotate(dir_x, dir_y):
	global direction
	direction[0] -= dir_x
	direction[1] -= dir_y

def move(dr):
	global r
	r += dr
	calculate()

def start_move(dir_r):
	global direction
	direction[2] += dir_r

def stop_move(dir_r):
	global direction
	direction[2] -= dir_r

def update(dt):
	rotate(
		direction[0]*dt,
		direction[1]*dt,
	)
	move(direction[2]*dt)

reset()
