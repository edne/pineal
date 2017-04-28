import logging
from contextlib import contextmanager
from math import pi
from pprint import pprint
from pineal.parser import parse

import pyglet.gl as gl
import pyglet.image
from pyglet.image.codecs.png import PNGImageDecoder

from pineal.shapes import solid_polygon, wired_polygon
from pineal.colors import color as color_

log = logging.getLogger(__name__)


_effects = {}
_primitives = {}


def effect(f):
    @contextmanager
    def decorated(arg):
        return f(arg)

    name = f.__name__
    _effects[name] = decorated

    return decorated


def apply_effect(f, name, arg):
    def changed(**kwargs):
        with _effects[name](arg):
            f(**kwargs)

    return changed


def primitive(f):
    name = f.__name__

    def decorated(**kwargs):
        changed = f
        for name, arg in kwargs.items():
            if name in _effects:
                changed = apply_effect(changed, name, arg)

        kwargs = {name: value
                  for (name, value) in kwargs.items()
                  if name not in _effects}

        changed(**kwargs)

    _primitives[name] = decorated
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


class Entity:
    def __init__(self, tree):
        if not isinstance(tree[0], str):
            raise Exception('Invalid Entity')

        name = tree[0]
        if name in _primitives:
            self.primitive = _primitives[name]
        else:
            raise Exception('Not implemented primitive')

        self.params = {branch[0]: branch[1]
                       for branch in tree[1]}
        pprint(self.params)

    def draw(self, ns):
        kwargs = {name: eval(leaf, ns)
                  for (name, leaf) in self.params.items()}

        self.primitive(**kwargs)


def pineal_eval(code, ns):
    tree = parse(code)
    log.debug(tree)

    entities = [Entity(branch) for branch in tree]

    def draw():
        for e in entities:
            e.draw(ns)

    from time import time

    ns.update({'draw': draw, 'time': time})
