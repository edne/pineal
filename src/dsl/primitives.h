PINEAL("cube")
void cube(double r){
	ofDrawBox(r);
}

PINEAL("polygon")
void polygon_n_r(int n, float r){
	static unordered_map<int, shared_ptr<ofPolyline>> polygons;
	shared_ptr<ofPolyline> p;

	if(polygons.find(n) == polygons.end()){
		p = make_shared<ofPolyline>();

		float angle, x, y;

		for(int i = 0; i < n; i++){
			angle = PI / 2 + i * TWO_PI / n;
			x = cos(angle);
			y = sin(angle);
			p->addVertex(ofPoint(x,y));
		}
		p->close();

		polygons[n] = p;
	}else{
		p = polygons[n];
	}
	ofPushMatrix();
	ofScale(r, r, r);
	p->draw();
	ofPopMatrix();
}

PINEAL("polygon")
void polygon_n(int n){
	polygon_n_r(n, 1);
}
