#include "pineal.h"

ofColor status_color;
double status_line_width = 1;
bool status_fill = true;


void background(double r, double g, double b, double a){
	ofBackground(r * 255, g * 255, b * 255, a * 255);
}

void color(py::object f, double r, double g, double b, double a){
	ofColor old_color = status_color;
	ofColor new_color = ofColor(r * 255, g * 255, b * 255, a * 255);

	status_color = new_color;
	ofSetColor(status_color);

	f();

	status_color = old_color;
	ofSetColor(status_color);
}

void __fill(py::object f, bool status){
	bool old_fill = status_fill;
	bool new_fill = status;

	status_fill = new_fill;
	if(status_fill){
		ofFill();
	}else{
		ofNoFill();
	}

	f();

	status_fill = old_fill;
	if(status_fill){
		ofFill();
	}else{
		ofNoFill();
	}
}

// TODO: use a namespace
void _fill(py::object f){
	__fill(f, true);
}

void no_fill(py::object f){
	__fill(f, false);
}

void line_width(py::object f, double new_width){
	double old_width = status_line_width;

	status_line_width = new_width;
	ofSetLineWidth(status_line_width);

	f();

	status_line_width = old_width;
	ofSetLineWidth(status_line_width);
}

void def_colors(){
	py::def("background", &background);
	py::def("color", &color);
	py::def("line_width", &line_width);
	py::def("fill", &_fill);
	py::def("no_fill", &no_fill);
}
