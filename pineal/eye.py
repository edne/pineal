import logging
import pyglet
import pineal.osc as osc
from pineal.lang import pineal_eval
from pineal.windows import new_renderer, new_master, new_overview

log = logging.getLogger(__name__)


def eye():
    log.info('Starting eye.py')

    vision = new_vision('')
    renderer = new_renderer(vision, [800, 800])

    new_master(renderer)
    new_overview(renderer)

    def callback(path, values):
        code = values[0]
        vision(code)

    osc.add_callback('/eye/code', callback)
    osc.start_server()

    pyglet.clock.schedule_interval(lambda dt: None, 1/120)
    pyglet.app.run()


def new_vision(code):
    stack = ['', code]
    namespace = {'draw': lambda: None}

    def eval_code(code):
        if code:
            pineal_eval(code, namespace)

    def load(code):
        eval_code(code)
        stack.append(code)

    def draw():
        if 'draw' not in namespace:
            eval_code(stack[-1])

        namespace['draw']()

    def vision(code=None):
        try:
            if code is not None:
                load(code)
            else:
                draw()
        except Exception as e:
            log.error(str(e))
            if stack:
                stack.pop()
            if stack:
                eval_code(stack[-1])

    return vision
