from color import Color, colorMode, fill, stroke, noFill, noStroke
from transformations import rotate, rotateX, rotateY, rotateZ, translate, scale, pushMatrix, popMatrix, resetMatrix
from solids import cube, tetrahedron, dodecahedron, octahedron
from shapes import square, line, point, quad, rect, triangle, polygon, circle, ellipse
#from lights import ambient, light, light_pos


#
import pyglet.gl as gl


def strokeWeight(w):
    gl.glLineWidth(w)
#


#
from random import uniform


def random(a=0, b=1):
    """ uniform distribution """
    return uniform(a,b)


def noise(a=1):
    """ white noise (uniform distribution in [-a,+a]) """
    return uniform(-a,a)
#
