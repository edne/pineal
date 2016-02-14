from core import log
from py.utils import hy_eval_code


class Vision(object):
    template = """
    (import core)
    (require py.dsl)
    (defn --draw-- [] {})
    """

    def __init__(self):
        self.history = []
        self.last_error = ""
        self.update("")

    def update(self, code):
        code = self.template.format(code)
        try:
            ns = {}
            hy_eval_code(code, ns)
            draw_function = ns["__draw__"]
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
