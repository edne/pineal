#pragma once

#include "ofMain.h"
#include "ofApp.h"
#include "ofLog.h"

class outApp : public ofBaseApp{
	public:
		outApp(shared_ptr<ofApp> main);
		void draw();

	private:
		shared_ptr<ofApp> main;
};
