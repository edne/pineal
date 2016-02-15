#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"

#include <boost/python.hpp>
namespace py = boost::python;

class pnEmbed{
	public:
		void setup(int argc, char ** argv);
		void update(string code);
		void draw();
	private:
		py::object vision;
		ofEasyCam camera;
};

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y);
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);

		int argc;
		char ** argv;

		pnEmbed embed;
		ofxOscReceiver oscReceiver;
};
