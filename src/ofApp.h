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
			lambda = [](){};
		}

		pEntity(py::object f){
			lambda = [=](){ f(); };
		}

		pEntity(function<void(void)> f){
			lambda = f;
		}

		void __call__(){
			lambda();
		}

		void operator()(){
			lambda();
		}

	private:
		function<void(void)> lambda;
};

class pAction{
	public:
		pAction(){  // by default identity
			lambda = [](pEntity& e){
				return e;
			};
		}

		pAction(function<pEntity(pEntity&)> a){
			lambda = a;
		}

		pEntity __call__(pEntity& e){
			return lambda(e);
		}

		pEntity operator()(pEntity& e){
			return lambda(e);
		}


	private:
		function<pEntity(pEntity&)> lambda;
};
