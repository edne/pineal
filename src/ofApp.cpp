#include "ofApp.h"
#include "dsl.h"

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
		{% for name in py_modules %}
			PyImport_AppendInittab("{{ name }}", &dsl::{{ name }}::init{{ name }});
		{% endfor %}

		vision = py::import("libs.vision").attr("Vision")();
	}catch(py::error_already_set){
		PyErr_Print();
	}

	ofSetVerticalSync(true);
	ofEnableDepthTest();
	ofEnableSmoothing();

	camera.setDistance(1);
	camera.setNearClip(0.01);

	ofSetEscapeQuitsApp(false);

	oscReceiver.setup(7172);
	oscClient.setup("localhost", 7173);  // frontend address, TODO: read config
	oscServer.setup("localhost", 7172);  // self

	int nOutputs = 2;
	int nInputs = 2;

	onset.setup();
	beat.setup();

	ofAddListener(onset.gotOnset, this, &ofApp::onsetEvent);
	ofAddListener(beat.gotBeat, this, &ofApp::beatEvent);

	ofSoundStreamSetup(nOutputs, nInputs, this);
}

void ofApp::exit(){
	ofSoundStreamStop();
	ofSoundStreamClose();
}

void ofApp::audioIn(float * input, int bufferSize, int nChannels){
	inBuf.allocate(bufferSize, nChannels);
	for(int i = 0; i < bufferSize * nChannels; i++){
		inBuf[i] = input[i];
	}

	onset.audioIn(input, bufferSize, nChannels);
	beat.audioIn(input, bufferSize, nChannels);
}

void ofApp::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);
		string address = m.getAddress();

		if(address == "/run-code"){
			dsl::colors::setup();

			string code = m.getArgAsString(0);
			try{
				vision.attr("update")(code);
			}catch(py::error_already_set){
				PyErr_Print();
			}
		}
		else if(address == "/ping"){
			ofxOscMessage m;
			m.setAddress("/ack");
			oscClient.sendMessage(m, false);
		}
		else if(address == "/exit"){
			std::exit(0);
		}
		else{
			// TODO: type check
			dsl::osc::set_float(address, m.getArgAsFloat(0));
		}
	}

	sendFloat("/amp", inBuf.getRMSAmplitude());
	sendFloat("/time", ofGetElapsedTimef());
}

void ofApp::draw(){
	output.allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
	output.begin();

	camera.begin();
	try{
		ofxOscMessage m;
		if(!vision.attr("draw")()){
			const char* error_msg = py::extract<const char*>(vision.attr("last_error"));
			m.addStringArg(error_msg);
			m.setAddress("/status/error");
		}else{
			ofxOscMessage m;
			m.setAddress("/status/working");
		}
		oscClient.sendMessage(m, false);
	}catch(py::error_already_set){
		PyErr_Print();
	}
	camera.end();

	output.end();

	int w = ofGetWidth();
	int h = ofGetHeight();
	int side = max(w, h);
	getTexture().draw((w - side) / 2,
	                  (h - side) / 2,
	                  side, side);

	string fps = "FPS: " + ofToString(ofGetFrameRate());
	ofSetColor(255);
	ofDrawBitmapString(fps, 10, 20);
}

void ofApp::sendFloat(string name, float x){
	ofxOscMessage msg;

	msg.setAddress(name);
	msg.addFloatArg(x);
	oscServer.sendMessage(msg, false);
}

ofTexture ofApp::getTexture(){
	return output.getTexture();
}

void ofApp::onsetEvent(float & time){
	// TODO: boolean OSC
}

void ofApp::beatEvent(float & time){
	// TODO: boolean OSC
}
