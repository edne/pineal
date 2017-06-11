import logging
from contextlib import contextmanager
import pyglet
import pyglet.gl as gl
import pineal.watcher as watcher

log = logging.getLogger(__name__)


def rendering_window(draw, h, w):
    window = pyglet.window.Window(width=w, height=h,
                                  visible=False)

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # gl.glEnable(gl.GL_LINE_SMOOTH)
    # gl.glEnable(gl.GL_POLYGON_SMOOTH)
    # gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
    # gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

    @window.event
    def on_draw():
        pyglet.clock.tick()

        window.clear()
        gl.glLoadIdentity()
        draw()

    pyglet.clock.set_fps_limit(30)
    pyglet.clock.schedule_interval(lambda dt: None, 1.0/30)


def eval_last(stack, ns):
    if stack:
        exec(stack[-1], ns)


@contextmanager
def safety(stack, ns):
    try:
        yield
    except Exception as e:
        log.error(str(e))
        if stack:
            stack.pop()
        eval_last(stack, ns)


def safe_eval(code, ns, stack):
    with safety(stack, ns):
        exec(code, ns)
        stack.append(code)


def render(file_name):
    with open(file_name) as f:
        initial_code = f.read()

    stack = [initial_code]
    ns = {}

    safe_eval(initial_code, ns, stack)
    watcher.add_callback(lambda code:
                         safe_eval(code, ns, stack))

    if 'draw' not in ns:
        raise Exception('No draw() function defined')

    def safe_draw():
        with safety(stack, ns):
            ns['draw']()

    rendering_window(safe_draw, 800, 800)
    pyglet.app.run()
