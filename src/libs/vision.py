from __future__ import print_function
from libs.utils import hy_eval_code


class Vision(object):
    template = """
    (require libs.dsl)
    (--header--)
    (defn --draw-- [] {})
    """

    def __init__(self):
        self.history = []
        self.ns = {}
        self.last_error = ""
        self.update("")

    def update(self, code):
        code = self.template.format(code)
        try:
            hy_eval_code(code, self.ns)
            self.history.append(code)
        except Exception, e:
            self.handle_error(e)

    def restore(self):
        if self.history:
            try:
                hy_eval_code(self.history[-1], self.ns)
            except Exception, e:
                self.handle_error(e)

    def draw(self):
        try:
            self.ns["__draw__"]()
        except Exception as e:
            if self.handle_error(e):
                self.ns["__draw__"]()

    def handle_error(self, error):
        if repr(error) != self.last_error:
            print(repr(error))  # TODO: something better
            self.last_error = repr(error)
        if self.history:
            self.history.pop()  # the broken one
            self.restore()
            return True
        else:
            return False
