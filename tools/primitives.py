import pyglet.gl as gl
import pyglet.image
from pyglet.image.codecs.png import PNGImageDecoder

from pineal.shapes import solid_polygon, wired_polygon
from .colors import color


psolid_memo = {}
pwired_memo = {}
image_memo = {}
layer_memo = {}


def psolid(n, c):
    def entity():
        if n not in psolid_memo:
            psolid_memo[n] = solid_polygon(n)

        vlist = psolid_memo[n]
        vlist.colors = color(c) * (n * 3)
        vlist.draw(gl.GL_TRIANGLES)

    return entity


def pwired(n, c):
    def entity():
        if n not in pwired_memo:
            pwired_memo[n] = wired_polygon(n)

        vlist = pwired_memo[n]
        vlist.colors = color(c) * n
        vlist.draw(gl.GL_LINE_LOOP)

    return entity


def image(name):
    def entity():
        if name not in image_memo:
            img = pyglet.image.load("images/%s.png" % name,
                                    decoder=PNGImageDecoder())
            image_memo[name] = img
            image_memo[name].blit(-1.0, 1.0, 0.0,
                                  2.0, 2.0)

    return entity


def on_layer(name, f):
    from pineal.framebuffer import Framebuffer

    if name not in layer_memo:
        layer_memo[name] = Framebuffer(800, 800)

    with layer_memo[name]:
        f()


def draw_layer(name):
    if name in layer_memo:
        layer_memo[name].texture.blit(-1, 1, 0,
                                      2, -2)
