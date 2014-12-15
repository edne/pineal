from color import Color, colorMode, fill, stroke, noFill, noStroke
from shapes import square
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
