import hy
from core import log
from py.hy_utils import eval_hy_code


class Vision(object):
    template = "(import [core [*]])(defn --draw-- [] {})"

    def __init__(self):
        self.history = []
        self.last_error = ""
        self.update("")

    def update(self, code):
        code = self.template.format(code)
        try:
            draw_function = eval_hy_code(code, {})
            self.history.append(draw_function)
        except Exception, e:
            self.handle_error(e)

    def draw(self):
        draw_function = self.history[-1]
        try:
            draw_function()
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, error):
        if repr(error) != self.last_error:
            log(repr(error))
            self.last_error = repr(error)
        if len(self.history) >= 2:
            self.history.pop()  # the broken one
            self.update(self.history.pop())
