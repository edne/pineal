#pragma once
#include "ofApp.h"

class Action{
	public:
		Action();
		Action(function<Entity(Entity&)> a);
		Entity __call__(Entity& e);
		Entity operator()(Entity e) const;

	private:
		function<Entity(Entity&)> apply;
};


