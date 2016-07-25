from __future__ import print_function
from libs.utils import hy_eval_code


class Vision(object):
    "Handle the compilation and the drawing of DSL code"

    template = """
    (require libs.dsl)
    (import [libs.dsl [*]])
    (--header--)
    (defn --draw-- [] {})
    """

    def __init__(self):
        "Create new vision"
        self.history = []
        self.ns = {}
        self.last_error = ""
        self.update("")

    def update(self, code):
        "Update with new code"
        code = self.template.format(code)
        try:
            hy_eval_code(code, self.ns)
            self.history.append(code)
        except Exception, e:
            self.handle_error(e)

    def restore(self):
        "Restore old working code"
        if self.history:
            try:
                hy_eval_code(self.history[-1], self.ns)
            except Exception, e:
                self.handle_error(e)

    def draw(self):
        "Drawing function, if there is an error return False"
        try:
            self.ns["__draw__"]()
            return True
        except Exception as e:
            if self.handle_error(e):
                self.ns["__draw__"]()
            else:
                self.update("")
            return False

    def handle_error(self, error):
        "Error handling: try to restore an old code, if fail return False"
        if repr(error) != self.last_error:
            self.last_error = repr(error)
        if self.history:
            self.history.pop()  # the broken one
            self.restore()
            return True
        else:
            return False
