from __future__ import print_function
from hy.lex import tokenize
from hy.compiler import hy_compile
from hy.importer import ast_compile


def hy_eval_code(source, namespace):
    "Eval Hy code from string"

    if "__name__" not in namespace:
        namespace["__name__"] = __name__

    tokens = tokenize(source)
    ast = hy_compile(tokens, "__pineal__")
    code = ast_compile(ast, "", "exec")
    eval(code, namespace)


def code_to_entity(source):
    "Get global group from code"
    template = """
    (require libs.dsl)
    (import [libs.dsl [*]])
    (--header--)

    (setv global-entities [])

    {}

    (setv global-group (make-entity (str "group")
                                    global-entities))
    """
    ns = {}
    source = template.format(source)
    hy_eval_code(source, ns)
    return ns["global_group"]


class Vision(object):
    "Handle the compilation and the drawing of DSL code"
    def __init__(self):
        "Create new vision"
        self.history = []
        self.last_error = ""
        self.update("")

    def update(self, code):
        "Update with new code"
        try:
            self.entity = code_to_entity(code)
            self.history.append(self.entity)
        except Exception, e:
            self.handle_error(e)

    def restore(self):
        "Restore old working code"
        if self.history:
            try:
                self.entity = self.history[-1]
            except Exception, e:
                self.handle_error(e)

    def draw(self):
        "Drawing function, if there is an error return False"
        try:
            self.entity()
            return True
        except Exception as e:
            if self.handle_error(e):
                self.entity()
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
