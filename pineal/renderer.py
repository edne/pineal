import logging
from contextlib import contextmanager
import pyglet
import pyglet.gl as gl
import pineal.osc as osc

log = logging.getLogger(__name__)


def rendering_window(draw, h, w):
    window = pyglet.window.Window(caption='(pineal renderer)',
                                  width=w,
                                  height=h,
                                  visible=False)

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    window.texture = None

    @window.event
    def on_draw():
        pyglet.clock.tick()
        window.clear()

        gl.glLoadIdentity()
        draw()

        buf = pyglet.image.get_buffer_manager().get_color_buffer()
        rawimage = buf.get_image_data()
        window.texture = rawimage.get_texture()

    return window


def pineal_eval(code, ns):
    def draw():
        exec(code, ns)

    ns.update({'draw': draw})


def eval_last(stack, namespace):
    if stack:
        pineal_eval(stack[-1], namespace)


@contextmanager
def safety(stack, namespace):
    try:
        yield
    except Exception as e:
        log.error(str(e))
        if stack:
            stack.pop()
        eval_last(stack, namespace)


def render():
    stack = ['']
    namespace = {}

    def callback(path, values):
        code = values[0]
        with safety(stack, namespace):
            pineal_eval(code, namespace)
            stack.append(code)

    def draw():
        with safety(stack, namespace):
            namespace['draw']()

    rendering_window(draw, 800, 800)

    osc.add_callback('/code', callback)
    osc.start_server()

    pyglet.clock.schedule_interval(lambda dt: None, 1/120)
    pyglet.app.run()
