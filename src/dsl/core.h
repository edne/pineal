#include "pineal.h"
#include "dsl/layers.h"
#include "dsl/colors.h"
#include "dsl/transformations.h"

void of_log(string s){
	ofLog() << s;
}

void cube(double r){
	ofDrawBox(r);
}

void def_core(){
	py::def("of_log", &of_log);
	py::def("cube", &cube);

	def_layers();
	def_colors();
	def_transformations();
}
