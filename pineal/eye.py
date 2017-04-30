import logging
from contextlib import contextmanager
import pyglet
import pineal.osc as osc
from pineal.lang import pineal_eval
from pineal.windows import new_renderer, new_master, new_overview

log = logging.getLogger(__name__)


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


def eye():
    stack = ['']
    namespace = {}

    def callback(path, values):
        code = values[0]
        with safety(stack, namespace):
            pineal_eval(code, namespace)
            stack.append(code)

    def draw():
        with safety(stack, namespace):
            if 'draw' not in namespace:
                eval_last(stack, namespace)

            namespace['draw']()

    renderer = new_renderer(draw, [800, 800])

    new_master(renderer)
    new_overview(renderer)

    osc.add_callback('/eye/code', callback)
    osc.start_server()

    pyglet.clock.schedule_interval(lambda dt: None, 1/120)
    pyglet.app.run()
