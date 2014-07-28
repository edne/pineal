import sys

import OpenGL.GLUT as glut
import pyglet.gl as gl
import pyglet

import camera
import windows


class Graphic:
    def __init__(self, visuals):
        glut.glutInit(sys.argv)  # for the 3d presets
        windows.create(visuals)

    def update(self):
        dt = pyglet.clock.tick()
        camera.update(dt)
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()

    def set_color(c, a=1.0):
        gl.glColor4f(c.r,c.g,c.b, a)
