#include "ofApp.h"

Entity::Entity(){
	draw = [](){};
}

Entity::Entity(py::object f){
	draw = [=](){ f(); };
}

Entity::Entity(function<void(void)> f){
	draw = f;
}

void Entity::__call__(){
	draw();
}

void Entity::operator()() const{
	draw();
}

