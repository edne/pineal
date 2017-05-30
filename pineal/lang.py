import logging
from contextlib import contextmanager
from math import pi

import pyglet.gl as gl
import pyglet.image
from pyglet.image.codecs.png import PNGImageDecoder

from pineal.shapes import solid_polygon, wired_polygon
from pineal.colors import color as color_

log = logging.getLogger(__name__)


_effects = {}


def effect(f):
    _effects.update({f.__name__: f})

    @contextmanager
    def decorated(fx_arg):
        return f(fx_arg)

    return decorated


class Primitive:
    def __init__(self, draw):
        self.draw = draw


def apply_effect(a, fx, fx_arg):
    def changed(*kargs, **kwargs):
        with fx(fx_arg):
            return a.draw()

    return Primitive(changed)


def primitive(f):
    def decorated(*kargs, **kwargs):
        def draw():
            f(*kargs, **kwargs)

        return Primitive(draw)

    return decorated


psolid_memo = {}
pwired_memo = {}
image_memo = {}
layer_memo = {}


@primitive
def polygon(sides, color, fill=True, **kwargs):
    if fill:
        if sides not in psolid_memo:
            psolid_memo[sides] = solid_polygon(sides)

        vlist = psolid_memo[sides]
        vlist.colors = color_(color) * (sides * 3)
        vlist.draw(gl.GL_TRIANGLES)
    else:
        if sides not in pwired_memo:
            pwired_memo[sides] = wired_polygon(sides)

        vlist = pwired_memo[sides]
        vlist.colors = color_(color) * sides
        vlist.draw(gl.GL_LINE_LOOP)


@primitive
def image(name):
    if name not in image_memo:
        img = pyglet.image.load("images/%s.png" % name,
                                decoder=PNGImageDecoder())
        image_memo[name] = img
        image_memo[name].blit(-1.0, 1.0, 0.0,
                              2.0, 2.0)


@primitive
def draw_layer(name):
    if name in layer_memo:
        layer_memo[name].texture.blit(-1, 1, 0,
                                      2, -2)


@effect
def scale(x):
    gl.glPushMatrix()
    gl.glScalef(x, x, x)
    yield
    gl.glPopMatrix()


@effect
def translate(x):
    gl.glPushMatrix()
    gl.glTranslatef(x, 0, 0)
    yield
    gl.glPopMatrix()


@effect
def rotate(angle):
    gl.glPushMatrix()
    gl.glRotatef(angle * 180 / pi,
                 0, 0, 1)
    yield
    gl.glPopMatrix()


@effect
def on_layer(name):
    from pineal.framebuffer import Framebuffer

    if name not in layer_memo:
        layer_memo[name] = Framebuffer(800, 800)

    with layer_memo[name]:
        yield


def pineal_eval(code, ns):
    def draw():
        exec(code, {})

    ns.update({'draw': draw})
