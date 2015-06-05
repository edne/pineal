import pyglet
from pyglet import clock
import pyglet.gl as gl
from config import RENDER_SIZE


render_texture = None


def getRenderTexture():
    return render_texture


def new_window(*args, **kwargs):
    window = pyglet.window.Window(*args, **kwargs)

    def update():
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
    window.update = update
    return window


def new_renderer(visions):
    """
    Offscreen windows where render stuff
    """
    W, H = RENDER_SIZE
    window = new_window(caption='(pineal renderer)',
                        fullscreen=0,
                        width=W,
                        height=H,
                        vsync=0,  # TODO: set to 1 after removing the while 1
                        visible=0)

    window.visions = visions

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    window.texture = None

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
    window.on_draw = on_draw

    old_update = window.update

    def update():
        old_update()
        print '\rfps: %3.1f' % clock.get_fps(),
    window.update = update

    return window


def new_output_window(*args, **kwargs):
    window = new_window(*args, **kwargs)

    def on_draw():
        w, h = window.width, window.height
        side = max(w, h)

        window.clear()
        if window.source.texture:
            window.source.texture.blit(-(side-w)/2,
                                       -(side-h)/2,
                                       0,
                                       side, side)

    window.on_draw = on_draw
    return window


def new_master(source):
    """
    Master output, on secondary monitor is exists, hidden otherwise
    """
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()

    # TODO: refactor this with a second monitor
    W, H = RENDER_SIZE
    if len(screens) > 1:
        window = new_window(caption='(pineal master)',
                            fullscreen=1,
                            screen=screens[-1],
                            vsync=1,
                            visible=1)
        window.set_mouse_visible(False)
    else:
        window = new_window(caption='(pineal master)',
                            fullscreen=0,
                            width=W,
                            height=H,
                            vsync=1,
                            visible=0)
    #
    window.source = source
    return window


def new_overview(source):
    """
    Overview for the programmer, nothing else to say
    """
    window = new_output_window(resizable=True,
                               caption='(pineal overview)',
                               width=600, height=450,
                               vsync=0)
    window.source = source
    return window
