PINEAL("cube")
void cube(double r){
	ofDrawBox(r);
}

PINEAL("polygon")
void polygon_n_r(int n, float r){
	ofPushMatrix();

	ofScale(r, r, r);
	ofRotateZ(90);

	ofSetCircleResolution(n);
	ofDrawCircle(0, 0, 1);

	ofPopMatrix();
}

PINEAL("polygon")
void polygon_n(int n){
	polygon_n_r(n, 1);
}
