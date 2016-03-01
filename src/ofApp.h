#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"

const int BUFFER_SIZE = 1366;

#include <boost/python.hpp>
namespace py = boost::python;

class ofApp : public ofBaseApp{
	public:
		ofApp(int argc, char ** argv);
		void setup();
		void update();
		void draw();

	private:
		int argc;
		char ** argv;

		ofxOscReceiver oscReceiver;

		py::object vision;
		ofEasyCam camera;
		ofFbo master;
};
