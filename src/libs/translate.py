from __future__ import print_function
from hy.lex import tokenize
from hy.compiler import hy_compile
from hy.importer import ast_compile


def hy_eval_code(code, namespace):
    "Eval Hy code from string"

    if "__name__" not in namespace:
        namespace["__name__"] = __name__

    tokens = tokenize(code)
    ast = hy_compile(tokens, "__pineal__")
    code = ast_compile(ast, "", "exec")
    eval(code, namespace)


def code_to_entity(code):
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
    code = template.format(code)
    hy_eval_code(code, ns)
    return ns["global_group"]


class Translator(object):
    "Translate code to entity"
    def __init__(self):
        "Create new translator"
        self.last_valid_code = ""

    def __call__(self, code):
        "Create with new code"
        try:
            e = code_to_entity(code)
            self.last_valid_code = code
            return e
        except Exception as error:
            print(error)
            return self.__call__(self.last_valid_code)
