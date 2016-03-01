PINEAL("scale")
void scale_xyz(py::object f, double x, double y, double z){
	ofPushMatrix();
	ofScale(x, y, z);
	f();
	ofPopMatrix();
}

PINEAL("scale")
void scale_xy(py::object f, double x, double y){
	scale_xyz(f, x, y, 1);
}

PINEAL("scale")
void scale_r(py::object f, double r){
	scale_xyz(f, r, r, r);
}

PINEAL("translate")
void translate_xyz(py::object f, double x, double y, double z){
	ofPushMatrix();
	ofTranslate(x, y, z);
	f();
	ofPopMatrix();
}

PINEAL("translate")
void translate_xy(py::object f, double x, double y){
	translate_xyz(f, x, y, 0);
}

PINEAL("translate")
void translate_x(py::object f, double x){
	translate_xyz(f, x, 0, 0);
}

PINEAL("rotate_x")
void rotate_x(py::object f, double rad){
	ofPushMatrix();
	ofRotateX(180 * rad / PI);
	f();
	ofPopMatrix();
}

PINEAL("rotate_y")
void rotate_y(py::object f, double rad){
	ofPushMatrix();
	ofRotateY(180 * rad / PI);
	f();
	ofPopMatrix();
}

PINEAL("rotate_z")
void rotate_z(py::object f, double rad){
	ofPushMatrix();
	ofRotateZ(180 * rad / PI);
	f();
	ofPopMatrix();
}

PINEAL("turn_x")
void turn_x(py::object f, int n){
	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		ofRotateX(360.0 / n);
	}
	ofPopMatrix();
}

PINEAL("turn_y")
void turn_y(py::object f, int n){
	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		ofRotateY(360.0 / n);
	}
	ofPopMatrix();
}

PINEAL("turn_z")
void turn_z(py::object f, int n){
	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		ofRotateZ(360.0 / n);
	}
	ofPopMatrix();
}
