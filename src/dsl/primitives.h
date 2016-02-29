namespace primitives{
	void cube(double r){
		ofDrawBox(r);
	}

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

	void polygon_n(int n){
		polygon_n_r(n, 1);
	}
}

void def_primitives(){
	py::def("cube", &primitives::cube);
	py::def("polygon", &primitives::polygon_n);
	py::def("polygon", &primitives::polygon_n_r);
}
