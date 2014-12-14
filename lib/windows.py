import pyglet
import pyglet.gl as gl


class Window(pyglet.window.Window):
    def __init__(self, visuals):
        self.visuals = visuals
        pyglet.window.Window.__init__(
            self,
            caption = '(pineal)',
            width = 800,
            height = 600,
            vsync = 1,
            visible = 1
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
            v.iteration()

    def update(self):
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
