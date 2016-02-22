#include "pineal.h"

unordered_map<string, shared_ptr<ofFbo>> layers;

void new_layer(string name){
	if(layers.find(name) != layers.end()){
		return;
	}
	auto fbo = make_shared<ofFbo>();

	fbo->allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
	fbo->begin();
	ofClear(255,255,255, 0);
	fbo->end();
	layers[name] = fbo;
}

void on_layer(py::object f, string name){
	if(layers.find(name) == layers.end()){
		new_layer(name);
	}
	ofEasyCam camera;
	camera.setDistance(1);
	camera.setNearClip(0.01);

	layers[name]->begin();
	camera.begin();
	f();
	camera.end();
	layers[name]->end();
}

void draw_layer(string name){
	if(layers.find(name) == layers.end()){
		new_layer(name);
	}
	layers[name]->getTexture().draw(-1, -1, 2, 2);
}

void def_layers(){
	py::def("on_layer", &on_layer);
	py::def("draw_layer", &draw_layer);
}
