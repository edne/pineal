#include "pineal.h"

void scale_xyz(py::object f, double x, double y, double z){
	ofPushMatrix();
	ofScale(x, y, z);
	f();
	ofPopMatrix();
}

void scale_xy(py::object f, double x, double y){
	scale_xyz(f, x, y, 1);
}

void scale_r(py::object f, double r){
	scale_xyz(f, r, r, r);
}

void translate_xyz(py::object f, double x, double y, double z){
	ofPushMatrix();
	ofTranslate(x, y, z);
	f();
	ofPopMatrix();
}

void translate_xy(py::object f, double x, double y){
	translate_xyz(f, x, y, 0);
}

void translate_x(py::object f, double x){
	translate_xyz(f, x, 0, 0);
}

void rotate_x(py::object f, double rad){
	ofPushMatrix();
	ofRotateX(180 * rad / PI);
	f();
	ofPopMatrix();
}

void rotate_y(py::object f, double rad){
	ofPushMatrix();
	ofRotateY(180 * rad / PI);
	f();
	ofPopMatrix();
}

void rotate_z(py::object f, double rad){
	ofPushMatrix();
	ofRotateZ(180 * rad / PI);
	f();
	ofPopMatrix();
}

void turn_x(py::object f, int n){
	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		ofRotateX(360.0 / n);
	}
	ofPopMatrix();
}

void turn_y(py::object f, int n){
	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		ofRotateY(360.0 / n);
	}
	ofPopMatrix();
}

void turn_z(py::object f, int n){
	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		ofRotateZ(360.0 / n);
	}
	ofPopMatrix();
}

void def_transformations(){
	py::def("scale", &scale_r);
	py::def("scale", &scale_xy);
	py::def("scale", &scale_xyz);

	py::def("translate", &translate_x);
	py::def("translate", &translate_xy);
	py::def("translate", &translate_xyz);

	py::def("rotate_x", &rotate_x);
	py::def("rotate_y", &rotate_y);
	py::def("rotate_z", &rotate_z);

	py::def("turn_x", &turn_x);
	py::def("turn_y", &turn_y);
	py::def("turn_z", &turn_z);
}
