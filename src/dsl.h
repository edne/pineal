#pragma once
#define PINEAL(_)

namespace dsl{
    {% for name in py_modules %}
        #include "dsl/{{ name }}.h"
    {% endfor %}

    BOOST_PYTHON_MODULE(core){
        py::class_<Entity>("Entity")
            .def(py::init<py::object>())
            .def("__call__", &Entity::__call__)
        ;

        py::class_<Action>("Action")
            .def("__call__", &Action::__call__)
        ;

        py::class_<Color>("Color");
    }
}
