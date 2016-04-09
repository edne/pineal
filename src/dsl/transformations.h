PINEAL("scale")
pAction scale_xyz(double x, double y, double z){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			ofPushMatrix();
			ofScale(x, y, z);
			e();
			ofPopMatrix();
		});
	});
}

PINEAL("translate")
pAction translate_xyz(double x, double y, double z){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			ofPushMatrix();
			ofTranslate(x, y, z);
			e();
			ofPopMatrix();
		});
	});
}

PINEAL("rotate_x")
pAction rotate_x(double rad){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			ofPushMatrix();
			ofRotateX(180 * rad / PI);
			e();
			ofPopMatrix();
		});
	});
}

PINEAL("rotate_y")
pAction rotate_y(double rad){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			ofPushMatrix();
			ofRotateY(180 * rad / PI);
			e();
			ofPopMatrix();
		});
	});
}

PINEAL("rotate_z")
pAction rotate_z(double rad){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			ofPushMatrix();
			ofRotateZ(180 * rad / PI);
			e();
			ofPopMatrix();
		});
	});
}

typedef enum{
	X, Y, Z
}Axis;

pAction turn(Axis axis, int n){
	return pAction([=](pEntity& e){
		return pEntity([=](){
			double rot;

			ofPushMatrix();
			for(int i=0; i<n; i++){
				e();
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
		});
	});
}

PINEAL("turn_x")
pAction turn_x(int n){
	return turn(X, n);
}

PINEAL("turn_y")
pAction turn_y(int n){
	return turn(Y, n);
}

PINEAL("turn_z")
pAction turn_z(int n){
	return turn(Z, n);
}
