from random import uniform
import pyglet.gl as gl
from color import Color, colorMode, fill, stroke, noFill, noStroke

import thirdparty.ezpyinline as ezpyinline


with open('pineal/livecoding/inline.c') as f:
    _ezc = ezpyinline.C(f.read())


def _vec(*args):
    return (gl.GLfloat * len(args))(*args)


def strokeWeight(w):
    gl.glLineWidth(w)


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


def random(a=0, b=1):
    """ uniform distribution """
    return uniform(a,b)


def noise(a=1):
    """ white noise (uniform distribution in [-a,+a]) """
    return uniform(-a,a)


# light
def ambient(amb):
    """ set ambiental light intensity """
    gl.glLightModelfv(
        gl.GL_LIGHT_MODEL_AMBIENT|gl.GL_LIGHT_MODEL_TWO_SIDE,
        _vec(amb,amb,amb, 1.0)
    )


def light(val):
    """ set light intensity """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, _vec(val, val, val, 1.0))


def light_pos(x,y,z):
    """ set light position """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, _vec(x,y,z, 3))
#


def cube(r=1):
    f = fill()
    s = stroke()
    _ezc.cube(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def tetrahedron(r=1):
    f = fill()
    s = stroke()
    _ezc.tetrahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def dodecahedron(r=1):
    f = fill()
    s = stroke()
    _ezc.dodecahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def octahedron(r=1):
    f = fill()
    s = stroke()
    _ezc.octahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


class Shape(object):
    def __init__(self):
        self._v = list()

    def vertex(self, x,y, z=0):
        self._v.append( (x,y,z) )


def createShape():
    return Shape()


def shape(s):
    s._draw()


def quad(l=1.0, x=0, y=0, z=0):
    f = fill()
    s = stroke()
    _ezc.quad(l,x,y,z, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)
