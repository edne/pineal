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


def expand(in_code, context={}):
    "Render code from template"
    template = Template(in_code)
    return template.render(context)


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
        out_code = expand(in_code, context)
        write_file(dest, out_code)


def get_modules():
    "Get name of DSL modules"  # TODO: get just names, not defines
    path = os.path.join(SOURCE, "dsl")
    files = [f for f in os.listdir(path) if f.endswith(".h")]

    modules = {}
    for m in files:
        name = os.path.splitext(m)[0]
        modules[name] = []

    return modules


def generate_dsl_wrapper(modules):
    "Generate dsl_wrapper.h"
    # TODO:
    # - generate an (empy) py module for each DSL module and import it in Hy
    # - move bindingls inside them from core

    code = Template("""
#pragma once
#define PINEAL(_)

namespace dsl{
{% for m_name in modules %}
#include "dsl/{{ m_name }}.h"{% endfor %}

BOOST_PYTHON_MODULE(core){
py::class_<pEntity>(\"pEntity\")
    .def(py::init<py::object>())
;

py::class_<pAction>(\"pAction\")
    .def(\"__call__\", &pAction::__call__)
;

py::class_<pColor>(\"pColor\");
{% for name, defines in modules.iteritems() %}
{% for py_func, c_func in defines %}
py::def("{{ py_func }}", &{{ name}}::{{ c_func }});{% endfor %}
{% endfor %}
}
}""").render({
        "modules": modules,
    })

    write_file(os.path.join("_src", "dsl_wrapper.h"), code)


def dsl_wrapper():
    "Replace old preprocessor, generate _src/dsl_wrpapper.h"
    modules = get_modules()

    def bind(m_name, py_func, c_func):
        modules[m_name].append((py_func, c_func))
        return ""

    navigate([], {"bind": bind})

    generate_dsl_wrapper(modules)


if __name__ == "__main__":
    # navigate()
    dsl_wrapper()
