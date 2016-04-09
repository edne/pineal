PINEAL("cube")
pEntity cube(double r){
	return pEntity([=](){
		ofDrawBox(r);
	});
}

PINEAL("polygon")
pEntity polygon_n_r(int n, float r){
	return pEntity([=](){
		ofPushMatrix();

		ofScale(r, r, r);
		ofRotateZ(90);

		ofSetCircleResolution(n);
		ofDrawCircle(0, 0, 1);

		ofPopMatrix();
	});
}

PINEAL("polygon")
pEntity polygon_n(int n){
	return polygon_n_r(n, 1);
}
