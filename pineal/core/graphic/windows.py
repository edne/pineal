from sys import argv

import OpenGL.GLUT as glut

import pyglet
from pyglet.window import key
import pyglet.gl as gl

from pineal.config import TITLE_OVERVIEW, FULLSCREEN, OUTPUT_SIZE, RENDER_SIZE

rendering = None


def vec(*args):
    return (gl.GLfloat * len(args))(*args)


class Overview(pyglet.window.Window):
    def __init__(self, visuals, **args):
        pyglet.window.Window.__init__(self, **args)

        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self):
        self.clear()

        if rendering.texture:
            rendering.texture.blit(0,0,0, self.width,self.height)

        self.fps_display.draw()


class Rendering(pyglet.window.Window):
    def __init__(self, visuals, **args):
        self.visuals = visuals
        pyglet.window.Window.__init__(self, **args)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glEnable( gl.GL_VERTEX_ARRAY )

        gl.glEnable( gl.GL_LINE_SMOOTH )
        gl.glEnable( gl.GL_POLYGON_SMOOTH )
        gl.glHint( gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST )
        gl.glHint( gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST )

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glShadeModel(gl.GL_SMOOTH)

        self.texture = None

    def on_draw(self):
        self.clear()
        predraw(*self.get_size())

        for v in self.visuals.values():
            gl.glMatrixMode(gl.GL_MODELVIEW)
            v.iteration()

        buf = pyglet.image.get_buffer_manager().get_color_buffer()

        rawimage = buf.get_image_data()
        #pitch = rawimage.width * len('RGBA')
        #pixels = rawimage.get_data('RGBA', pitch)

        # li controllo da gui e F.O.
        #postprocessing.mirror(pixels, rawimage.width, rawimage.height)

        self.texture = rawimage.get_texture()


class Master(pyglet.window.Window):
    def __init__(self, visuals, **args):
        pyglet.window.Window.__init__(self, **args)

    def on_draw(self):
        self.clear()
        if rendering.texture:
            rendering.texture.blit(0,0,0, self.width,self.height)


def predraw(w,h):
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,vec(1,1,10, 3))
    gl.glLightModelfv(
        gl.GL_LIGHT_MODEL_AMBIENT|gl.GL_LIGHT_MODEL_TWO_SIDE,
        vec(1,1,1, 1.0)
    )

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    #glOrtho(-1, 1, -1, 1, -1, 1)
    #(w,h) = self.get_size()
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


def init(visuals):
    glut.glutInit(argv)  # for the 3d presets

    global rendering, overview, master

    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()

    overview = Overview(
        visuals,
        caption = TITLE_OVERVIEW,
        width = 600, height = 450,
        vsync = 0
    )

    rendering = Rendering(
        visuals,
        caption = 'rendering',
        width = RENDER_SIZE[0],
        height = RENDER_SIZE[1],
        vsync = 0,
        visible = 0
    )

    if FULLSCREEN:
        if len(screens)>1:
            master = Master(
                visuals,
                caption = "Master",
                screen = screens[-1],
                fullscreen = 1,
                vsync = 1,
                visible = 1,
            )
            master.set_mouse_visible(False)
    else:
        master = Master(
            visuals,
            caption = "Master",
            width = OUTPUT_SIZE[0],
            height = OUTPUT_SIZE[1],
            vsync = 1,
            visible = 1,
        )
        master.set_mouse_visible(False)


def update():
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
