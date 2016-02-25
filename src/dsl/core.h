#include "pineal.h"
#include "dsl/layers.h"
#include "dsl/colors.h"
#include "dsl/transformations.h"

void of_log(string s){
	ofLog() << s;
}

void cube(double r){
	ofDrawBox(r);
}

unordered_map<int, shared_ptr<ofPolyline>> polygons;

void _polygon(int n, float r){
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

void polygon(int n){
	_polygon(n, 1);
}

void def_core(){
	py::def("of_log", &of_log);
	py::def("cube", &cube);
	py::def("polygon", &_polygon);
	py::def("polygon", &polygon);

	def_layers();
	def_colors();
	def_transformations();
}
