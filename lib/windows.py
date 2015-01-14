import pyglet
from pyglet import clock
import pyglet.gl as gl


class Renderer(pyglet.window.Window):
    def __init__(self, visuals):
        self.visuals = visuals

        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screens = display.get_screens()

        if len(screens) > 1:
            pyglet.window.Window.__init__(
                self,
                caption = '(pineal master)',
                fullscreen = 1,
                screen = screens[-1],
                vsync = 1,
                visible = 1
            )
            self.set_mouse_visible(False)
        else:
            pyglet.window.Window.__init__(
                self,
                caption = '(pineal master)',
                fullscreen = 0,
                width = 800,
                height = 600,
                vsync = 1,
                visible = 0
            )

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glEnable( gl.GL_LINE_SMOOTH )
        gl.glEnable( gl.GL_POLYGON_SMOOTH )
        gl.glHint( gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST )
        gl.glHint( gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST )

        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glShadeModel(gl.GL_SMOOTH)

        self.texture = None

    def on_draw(self):
        self.clear()

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        #glOrtho(-1, 1, -1, 1, -1, 1)
        (w,h) = self.get_size()
        gl.glScalef(
            float(min(w,h))/w,
            -float(min(w,h))/h,
            1
        )

        gl.gluPerspective(45.0, 1, 0.1, 1000.0)
        gl.gluLookAt(
            0,0,2.4,  # 2.4 = (4.0/3)/math.tan(45.0/2)
            0,0,0,
            0,1,0
        )

        for v in self.visuals.values():
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            v.iteration()

        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        rawimage = buf.get_image_data()
        self.texture = rawimage.get_texture()

        clock.tick()

    def update(self):
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
        print '\rfps: %3.1f' % clock.get_fps(),


class Overview(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(
            self,
            caption = '(pineal overview)',
            width = 600, height = 450,
            vsync = 0
        )
        self.texture = None
        #self.fps_display = pyglet.clock.ClockDisplay()  # segfaults

    def on_draw(self):
        self.clear()
        if self.texture:
            self.texture.blit(0,0,0, self.width,self.height)
            #self.fps_display.draw()

    def update(self, texture):
        self.texture = texture
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
