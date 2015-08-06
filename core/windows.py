import pyglet
import pyglet.gl as gl


def new_window(*args, **kwargs):
    window = pyglet.window.Window(*args, **kwargs)
    return window


def new_renderer(visions, size):
    """
    Offscreen windows where render stuff
    """
    W, H = size
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

    # pyglet.clock.schedule_interval(window.update, 1.0/128.0)
    # pyglet.clock.set_fps_limit(30)

    @window.event
    def on_draw():
        pyglet.clock.tick()
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

        for v in window.visions.values():
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            v.iteration()

        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        rawimage = buf.get_image_data()
        window.texture = rawimage.get_texture()

    return window


def output_draw(window):
    w, h = window.width, window.height
    side = max(w, h)
    texture = window.source.texture

    window.clear()
    if texture:
        texture.blit(-(side-w)/2,
                     -(side-h)/2,
                     0,
                     side, side)


def new_output_window(*args, **kwargs):
    window = new_window(*args, **kwargs)

    @window.event
    def on_draw():
        output_draw(window)
    return window


def new_master(source):
    """
    Master output, on secondary monitor is exists, hidden otherwise
    """
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()

    window = new_output_window(caption='(pineal master)',
                               resizable=True,
                               screen=screens[-1])
    window.source = source
    return window


def new_overview(source):
    """
    Overview for the programmer, nothing else to say
    """
    fps = pyglet.clock.ClockDisplay()
    window = new_output_window(resizable=True,
                               caption='(pineal overview)',
                               width=600,
                               height=450)

    @window.event
    def on_draw():
        output_draw(window)
        fps.draw()

    window.source = source
    return window
