import sys

import OpenGL.GLUT as glut
import pyglet.gl as gl
import pyglet

import camera,windows


class Graphic:
    def __init__(self):
        glut.glutInit(sys.argv)  # for the 3d presets
        windows.create()

    def update(self):
        dt = pyglet.clock.tick()
        camera.update(dt)
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()


graphic = None # TODO: that's HORRIBLE


def init():
    global graphic
    graphic = Graphic()


def update():
    graphic.update()


def set_color(c, a=1.0):
    gl.glColor4f(c.r,c.g,c.b, a)
