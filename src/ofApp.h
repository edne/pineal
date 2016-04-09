#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"
#include "ofxAubio.h"

const int BUFFER_SIZE = 1366;

#include <boost/python.hpp>
namespace py = boost::python;

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

		py::object vision;
		ofEasyCam camera;
		ofFbo master;

		ofxAubioOnset onset;
		ofxAubioBeat beat;
};

class pEntity{
	public:
		pEntity(){
			draw = [](){};
		}

		pEntity(py::object f){
			draw = [=](){ f(); };
		}

		pEntity(function<void(void)> f){
			draw = f;
		}

		void operator()() const{
			draw();
		}

	private:
		function<void(void)> draw;
};

class pAction{
	public:
		pAction(){  // by default identity
			apply = [](pEntity& e){
				return e;
			};
		}

		pAction(function<pEntity(pEntity&)> a){
			apply = a;
		}

		pEntity __call__(pEntity& e){
			return apply(e);
		}

	private:
		function<pEntity(pEntity&)> apply;
};
