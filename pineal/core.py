import logging
from contextlib import contextmanager
from math import pi

import pyglet.gl as gl
import pyglet.image
from pyglet.image.codecs.png import PNGImageDecoder

from pineal.shapes import solid_polygon, wired_polygon
from pineal.framebuffer import Framebuffer


log = logging.getLogger(__name__)


_effects = {}


def effect(f):
    @contextmanager
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)

    _effects.update({f.__name__: decorated})
    return decorated


class Entity:
    def __init__(self, draw):
        self.draw = draw

    def __getattr__(self, attr):
        fx = _effects[attr]

        def method(*args, **kwargs):
            def new_draw():
                with fx(*args, **kwargs):
                    return self.draw()

            return Entity(new_draw)

        return method


def primitive(f):
    def decorated(*args, **kwargs):
        def draw():
            f(*args, **kwargs)

        return Entity(draw)

    return decorated


def make_color(x):
    "try to cast x to (r, g, b, a)"

    if len(x) == 4:
        return tuple(x)

    elif len(x) == 3:
        return tuple(x) + (1, )

    else:
        raise TypeError("Invalid color")


psolid_memo = {}
pwired_memo = {}
image_memo = {}
layer_memo = {}
windows_memo = []


@primitive
def polygon(sides, color, fill=True):
    if fill:
        if sides not in psolid_memo:
            psolid_memo[sides] = solid_polygon(sides)

        vlist = psolid_memo[sides]
        vlist.colors = make_color(color) * (sides * 3)
        vlist.draw(gl.GL_TRIANGLES)
    else:
        if sides not in pwired_memo:
            pwired_memo[sides] = wired_polygon(sides)

        vlist = pwired_memo[sides]
        vlist.colors = make_color(color) * sides
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
def layer(name):
    if name in layer_memo:
        layer_memo[name].texture.blit(-1, 1, 0,
                                      2, -2)


@effect
def scale(x, y=None, z=None):
    if y is None:
        y, z = x, x
    elif z is None:
        z = 1

    gl.glPushMatrix()
    gl.glScalef(x, y, z)
    yield
    gl.glPopMatrix()


@effect
def translate(x, y=0, z=0):
    gl.glPushMatrix()
    gl.glTranslatef(x, y, z)
    yield
    gl.glPopMatrix()


@effect
def rotate(angle, axis=(0, 0, 1)):
    gl.glPushMatrix()
    gl.glRotatef(angle * 180 / pi, *axis)
    yield
    gl.glPopMatrix()


@effect
def on_layer(name):
    if name not in layer_memo:
        layer_memo[name] = Framebuffer(800, 800)

    with layer_memo[name]:
        yield


@effect
def window(name, show_fps=False):
    with on_layer(name):
        yield

    if name in windows_memo:
        return

    windows_memo.append(name)
    win = pyglet.window.Window(resizable=True)

    # TODO: hanldle show_fps changed runtime
    if show_fps:
        fps = pyglet.clock.ClockDisplay()

    @win.event
    def on_draw():
        w, h = win.width, win.height
        side = max(w, h)

        win.clear()

        layer(name)\
            .scale(side/2.0, -side/2.0)\
            .translate(w/2, h/2)\
            .draw()

        if show_fps:
            fps.draw()

    @win.event
    def on_close():
        windows_memo.remove(name)

    @win.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED


def stroke_weight(w):
    "OpenGL lines width"
    # TODO: make it an effect
    gl.glLineWidth(w)
