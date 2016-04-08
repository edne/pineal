PINEAL("scale_")
pAction scale(double x, double y, double z){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			ofPushMatrix();
			ofScale(x, y, z);
			e.draw();
			ofPopMatrix();
		});
	});
}

PINEAL("scale")
void scale_xyz(pEntity& f, double x, double y, double z){
	ofPushMatrix();
	ofScale(x, y, z);
	f();
	ofPopMatrix();
}

PINEAL("scale")
void scale_xy(pEntity& f, double x, double y){
	scale_xyz(f, x, y, 1);
}

PINEAL("scale")
void scale_r(pEntity& f, double r){
	scale_xyz(f, r, r, r);
}

PINEAL("translate")
void translate_xyz(pEntity& f, double x, double y, double z){
	ofPushMatrix();
	ofTranslate(x, y, z);
	f();
	ofPopMatrix();
}

PINEAL("translate")
void translate_xy(pEntity& f, double x, double y){
	translate_xyz(f, x, y, 0);
}

PINEAL("translate")
void translate_x(pEntity& f, double x){
	translate_xyz(f, x, 0, 0);
}

PINEAL("rotate_x")
void rotate_x(pEntity& f, double rad){
	ofPushMatrix();
	ofRotateX(180 * rad / PI);
	f();
	ofPopMatrix();
}

PINEAL("rotate_y")
void rotate_y(pEntity& f, double rad){
	ofPushMatrix();
	ofRotateY(180 * rad / PI);
	f();
	ofPopMatrix();
}

PINEAL("rotate_z")
void rotate_z(pEntity& f, double rad){
	ofPushMatrix();
	ofRotateZ(180 * rad / PI);
	f();
	ofPopMatrix();
}

typedef enum{
	X, Y, Z
}Axis;

void turn(pEntity& f, Axis axis, int n){
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
void turn_x(pEntity& f, int n){
	turn(f, X, n);
}

PINEAL("turn_y")
void turn_y(pEntity& f, int n){
	turn(f, Y, n);
}

PINEAL("turn_z")
void turn_z(pEntity& f, int n){
	turn(f, Z, n);
}

PINEAL("recursion_c")
void recursion(int depth, pEntity& entity, py::list& actions){
	if(depth > 0){
		entity();

		for(int i=0; i<py::len(actions); i++){
			py::object a = actions[i];
			pEntity applied([&](){ a(entity); });

			recursion(depth - 1, applied, actions);
		}
	}
}
