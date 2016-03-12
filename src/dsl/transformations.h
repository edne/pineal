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

typedef enum{
	X, Y, Z
}Axis;

void turn(py::object f, Axis axis, int n){
	double rot;

	ofPushMatrix();
	for(int i=0; i<n; i++){
		f();
		rot = 360.0 / n;
		if(axis == X){
			ofRotateX(rot);
		}else if(axis == Y){
			ofRotateY(rot);
		}else if(axis == Z){
			ofRotateZ(rot);
		}
	}
	ofPopMatrix();
}

PINEAL("turn_x")
void turn_x(py::object f, int n){
	turn(f, X, n);
}

PINEAL("turn_y")
void turn_y(py::object f, int n){
	turn(f, Y, n);
}

PINEAL("turn_z")
void turn_z(py::object f, int n){
	turn(f, Z, n);
}
