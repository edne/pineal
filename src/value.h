#pragma once
#include "ofApp.h"

class Value{
	public:
		Value();
		Value(float x);
		Value(py::list args, int index, Value default_value);
		Value(py::list args, int index, float default_value) :
			Value(args, index, Value(default_value)) {
		};
		float operator()() const;

    private:
		float value;
};


