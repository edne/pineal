import pyglet
from pyglet import clock
import pyglet.gl as gl
from config import RENDER_SIZE


render_texture = None


def getRenderTexture():
    return render_texture


def new_window(*args, **kwargs):
    window = pyglet.window.Window(*args, **kwargs)
    return window


def new_renderer(visions):
    """
    Offscreen windows where render stuff
    """
    W, H = RENDER_SIZE
    window = new_window(caption='(pineal renderer)',
                        width=W,
                        height=H,
                        visible=0)

    window.visions = visions

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    window.texture = None

    @window.event
    def on_draw():
        window.clear()

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        (w, h) = window.get_size()
        gl.glScalef(
            float(min(w, h))/w,
            -float(min(w, h))/h,
            1
        )

        gl.gluPerspective(45.0, 1, 0.1, 1000.0)
        gl.gluLookAt(0, 0, 2.4,
                     0, 0, 0,
                     0, 1, 0)

        global render_texture
        render_texture = window.texture

        for v in window.visions.values():
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            v.iteration()

        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        rawimage = buf.get_image_data()
        window.texture = rawimage.get_texture()

        clock.tick()
        print '\rfps: %3.1f' % clock.get_fps(),
    return window


def new_output_window(*args, **kwargs):
    window = new_window(*args, **kwargs)

    @window.event
    def on_draw():
        w, h = window.width, window.height
        side = max(w, h)
        texture = window.source.texture

        window.clear()
        if texture:
            texture.blit(-(side-w)/2,
                         -(side-h)/2,
                         0,
                         side, side)
    return window


def new_master(source):
    """
    Master output, on secondary monitor is exists, hidden otherwise
    """
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()

    dual_screen = 0 * len(screens) > 1
    window = new_output_window(caption='(pineal master)',
                               fullscreen=dual_screen,
                               screen=screens[-1],
                               visible=dual_screen)
    window.source = source
    return window


def new_overview(source):
    """
    Overview for the programmer, nothing else to say
    """
    window = new_output_window(resizable=True,
                               caption='(pineal overview)',
                               width=600,
                               height=450)
    window.source = source
    return window
