#!/usr/bin/env python
from __future__ import print_function
import os
from jinja2 import Template

SOURCE = "src"
DEST = "_src"


def read_file(file_name):
    "Read a file"
    with open(file_name) as f:
        return f.read()


def write_file(file_name, content):
    "Write a file"
    with open(file_name, "w") as f:
        f.write(content)


def navigate(path=[], context={}):
    "Explore file tree expanding each file"

    source = os.path.join(* [SOURCE] + path)
    dest = os.path.join(* [DEST] + path)

    if os.path.isdir(source):
        if not os.path.exists(dest):
            os.makedirs(dest)

        for f in os.listdir(source):
            navigate(path + [f], context)
    else:
        in_code = read_file(source)
        out_code = Template(in_code).render(context)
        write_file(dest, out_code)


def get_modules():
    "Get name of DSL modules"
    path = os.path.join(SOURCE, "dsl")
    files = [f for f in os.listdir(path) if f.endswith(".h")]

    modules = []
    for f in files:
        name = os.path.splitext(f)[0]
        modules.append(name)

    return modules


def dsl_bind():
    "Do the actual bindings"
    modules = get_modules()
    context = {}
    context["py_modules"] = modules
    context["module"] = {}

    def begin_module(name):
        context["module"]["bindings"] = []  # list of tuples

        def bind(py_func, c_func):
            context["module"]["bindings"].append((py_func, c_func))
            return ""

        context["module"]["bind"] = bind
        context["module"]["name"] = name
        return Template("namespace {{ module.name }}{").render(context)

    context["begin_module"] = begin_module

    def end_module():
        return Template("""
    BOOST_PYTHON_MODULE({{ module.name }}){
        {% for py_func, c_func in module.bindings %}
            py::def("{{ py_func }}", &{{ c_func }});
        {% endfor %}
    }
}
""").render(context)

    context["end_module"] = end_module

    navigate([], context)


if __name__ == "__main__":
    dsl_bind()
