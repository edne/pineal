import sys
sys.argv = sys.argv[:1] + ['-ckivy:log_level:error', '--size=640x480']
import kivy.graphics.opengl as gl

import windows


# TODO Graphic as kivy App
class Graphic:
    def __init__(self, visuals):
        windows.init(visuals)

    def update(self):
        #dt = pyglet.clock.tick()
        windows.update()

    def run(self):
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            pass

    def set_color(c, a=1.0):
        gl.glColor4f(c.r,c.g,c.b, a)
