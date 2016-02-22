#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"

const int BUFFER_SIZE = 1366;

#include <boost/python.hpp>
namespace py = boost::python;

class Embed{
	public:
		Embed(int argc, char ** argv);
		void setup();
		void update(string code);
		void draw();
		ofTexture getBuffer();

	private:
		int argc;
		char ** argv;

		py::object vision;
		ofEasyCam camera;
		ofFbo master;
};

class Renderer : public ofBaseApp{
	public:
		Renderer(int argc, char ** argv);
		void setup();
		void update();
		void draw();

	private:
		ofxOscReceiver oscReceiver;
		shared_ptr<Embed> embed;
};
