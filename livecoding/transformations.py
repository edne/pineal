import pyglet.gl as gl
import thirdparty.ezpyinline as ezpyinline


with open('livecoding/c/transformations.c') as f:
    _ezc = ezpyinline.C(f.read())


def rotateX(angle):
    rotate(angx = angle)


def rotateY(angle):
    rotate(angy = angle)


def rotateZ(angle):
    rotate(angz = angle)


def rotate(angz=0, angy=0, angx=0):
    _ezc.rotate(angx,angy,angz)


def translate(x=0, y=0, z=0):
    _ezc.translate(x, y, z)


def scale(x, y=None, z=1):
    if not y:
        y = x
    _ezc.scale(x, y, z)

_matrix_stack = 0


def pushMatrix():
    global _matrix_stack
    if _matrix_stack<30:
        _ezc.push()
        _matrix_stack += 1
    else:
        print "TOO many push()"
        raise Exception()


def popMatrix():
    global _matrix_stack
    if _matrix_stack>0:
        _ezc.pop()
    else:
        print "TOO many pop()"
        raise Exception()
    _matrix_stack -= 1 # if goes to -1 i can handle it


def resetMatrix():
    global _matrix_stack
    _matrix_stack = 0
    gl.glLoadIdentity()
