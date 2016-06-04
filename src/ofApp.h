#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"
#include "ofxAubio.h"

const int BUFFER_SIZE = 1366;

#include <boost/python.hpp>
namespace py = boost::python;

#include "lang.h"

class ofApp : public ofBaseApp{
	public:
		ofApp(int argc, char ** argv);
		void setup();
		void update();
		void exit();
		void draw();

		ofTexture getTexture();

		void audioIn(float * input, int bufferSize, int nChannels);

		void onsetEvent(float & time);
		void beatEvent(float & time);

	private:
		int argc;
		char ** argv;

		ofFbo output;

		ofxOscReceiver oscReceiver;
		ofxOscSender oscClient;
		ofxOscSender oscServer;

		py::object vision;
		ofEasyCam camera;
		ofFbo master;

		bool osc_beat;
		ofxAubioOnset onset;
		ofxAubioBeat beat;
};
