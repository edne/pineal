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
