#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"

#include <boost/python.hpp>
namespace py = boost::python;

class Embed{
	public:
		Embed(int size, int argc, char ** argv);
		void setup();
		void update(string code);
		void draw();
		ofTexture getBuffer();

	private:
		int size;
		int argc;
		char ** argv;

		py::object vision;
		ofEasyCam camera;
		ofFbo fbo;
};

class Renderer : public ofBaseApp{
	public:
		Renderer(int size, int argc, char ** argv);
		void setup();
		void update();
		void draw();

	private:
		ofxOscReceiver oscReceiver;
		shared_ptr<Embed> embed;
};
