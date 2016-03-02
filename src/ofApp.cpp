#include "ofApp.h"
#include "dsl_wrapper.h"

ofApp::ofApp(int argc, char ** argv){
	this->argc = argc;
	this->argv = argv;
}

void ofApp::setup(){
	ofLog() << "Running setup()";

	try{
		Py_Initialize();
		PySys_SetArgv(argc, argv);

		PyImport_AppendInittab("core", &dsl::initcore);

		vision = py::import("py.vision").attr("Vision")();
	}catch(py::error_already_set){
		PyErr_Print();
	}

	ofSetVerticalSync(true);
	ofEnableDepthTest();

	camera.setDistance(1);
	camera.setNearClip(0.01);

	master.allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
	master.begin();
	ofClear(255,255,255, 0);
	master.end();

	ofSetColor(255);
	ofFill();
	ofSetLineWidth(1);

	ofSetEscapeQuitsApp(false);
	oscReceiver.setup(7172);
}

void ofApp::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);

		if(m.getAddress() == "/code"){
			string code = m.getArgAsString(0);
			ofLog() << "OSC mesage:" << endl << "/code" << endl << code;
			try{
				vision.attr("update")(code);
			}catch(py::error_already_set){
				PyErr_Print();
			}
		}
	}
}

void ofApp::draw(){
	master.begin();
	camera.begin();
	try{
		vision.attr("draw")();
	}catch(py::error_already_set){
		PyErr_Print();
	}
	camera.end();
	master.end();

	auto texture = master.getTexture();

	int w = ofGetWindowWidth();
	int h = ofGetWindowHeight();
	texture.draw(0, -(w - h) / 2, w, w);

	string fps = "FPS: " + ofToString(ofGetFrameRate());
	ofSetColor(255);
	ofDrawBitmapString(fps, 10, 20);
}
