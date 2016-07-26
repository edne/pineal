#pragma once

#include "ofMain.h"
#include "pineal.h"
#include "ofLog.h"

class outApp : public ofBaseApp{
	public:
		outApp(shared_ptr<Pineal> main);
		void draw();

	private:
		shared_ptr<Pineal> main;
};
