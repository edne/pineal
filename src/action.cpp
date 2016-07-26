#include "ofApp.h"

Action::Action(){  // by default identity
	apply = [](Entity& e){
		return e;
	};
}

Action::Action(function<Entity(Entity&)> a){
	apply = a;
}

Entity Action::__call__(Entity& e){
	return apply(e);
}

Entity Action::operator()(Entity e) const{
	return apply(e);
}
