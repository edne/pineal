PINEAL("cube")
pEntity cube(py::list args){
	float r;

	if(py::len(args) > 0){
		r = py::extract<float>(args[0]);
	}else{
		r = 0.5;
	}

	return pEntity([=](){
		ofDrawBox(r);
	});
}

PINEAL("polygon")
pEntity polygon_n_r(py::list args){
	int n;
	float r;

	if(py::len(args) > 0){
		n = py::extract<int>(args[0]);
	}else{
		// TODO: Raise Python exception
		return pEntity();
	}

	if(py::len(args) > 1){
		r = py::extract<float>(args[1]);
	}else{
		r = 0.5;
	}

	return pEntity([=](){
		ofPushMatrix();

		ofScale(r, r, r);
		ofRotateZ(90);

		ofSetCircleResolution(n);
		ofDrawCircle(0, 0, 1);

		ofPopMatrix();
	});
}
