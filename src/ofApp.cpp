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
	oscSender.setup("localhost", 7173);  // frontend address, TODO: read config

	int nOutputs = 2;
	int nInputs = 2;

	osc_beat = false;
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
	onset.audioIn(input, bufferSize, nChannels);
	beat.audioIn(input, bufferSize, nChannels);

	ofSoundBuffer inBuf;
	inBuf.allocate(bufferSize, nChannels);

	for(int i = 0; i < bufferSize * nChannels; i++){
		inBuf[i] = input[i];
	}

	dsl::audio::set_inBuf(inBuf);
}

void ofApp::update(){
	dsl::audio::update();

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
		if(address == "/ping"){
			ofxOscMessage m;
			m.setAddress("/ack");
			oscSender.sendMessage(m, false);
		}
		if(address == "/exit"){
			std::exit(0);
		}
		if(address == "/beat/enable"){
			osc_beat = m.getArgAsBool(0);
			ofLog() << "Toggled /beat/enable to " << osc_beat;
		}
		if(address == "/beat" && osc_beat){
			dsl::audio::set_beat();
		}
		if(dsl::osc::exists_value(address)){
			// TODO: type check
			dsl::osc::set_value(address, m.getArgAsFloat(0));
		}
	}
}

void ofApp::draw(){
	output.allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
	output.begin();

	camera.begin();
	try{
		vision.attr("draw")();
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

ofTexture ofApp::getTexture(){
	return output.getTexture();
}

void ofApp::onsetEvent(float & time){
	dsl::audio::set_onset();
}

void ofApp::beatEvent(float & time){
	if(!osc_beat){
		dsl::audio::set_beat();
	}
}
