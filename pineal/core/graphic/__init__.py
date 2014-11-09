import OpenGL.GLUT as glut
import pyglet.gl as gl
import pyglet

import camera
import windows


class Graphic:
    def __init__(self, visuals):
        windows.init(visuals)

    def update(self):
        dt = pyglet.clock.tick()
        camera.update(dt)
        windows.update()
        
    def run(self):
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            pass

    def set_color(c, a=1.0):
        gl.glColor4f(c.r,c.g,c.b, a)
