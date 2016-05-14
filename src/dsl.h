#pragma once
#define PINEAL(_)

namespace dsl{
    {% for name in py_modules %}
        #include "dsl/{{ name }}.h"
    {% endfor %}

    BOOST_PYTHON_MODULE(core){
        py::class_<pEntity>("pEntity")
            .def(py::init<py::object>())
        ;

        py::class_<pAction>("pAction")
            .def("__call__", &pAction::__call__)
        ;

        py::class_<pColor>("pColor");
    }
}
