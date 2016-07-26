#pragma once
#include "ofApp.h"

class Entity{
	public:
		Entity();
		Entity(py::object f);
		Entity(function<void(void)> f);

        void __call__();
		void operator()() const;

	private:
		function<void(void)> draw;
};

