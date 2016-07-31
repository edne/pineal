#include "pineal.h"


namespace dsl{
    BOOST_PYTHON_MODULE(core){
        py::class_<Entity>("Entity")
            .def(py::init<py::object>())
            .def("__call__", &Entity::__call__)
        ;
		py::def("make_entity", &make_entity);

        py::class_<Action>("Action")
            .def("__call__", &Action::__call__)
        ;
		py::def("make_action", &make_action);

        py::class_<Color>("Color");
		py::def("make_color", &make_color);

        py::class_<Value>("Value")
            .def(py::init<float>())
            .def("__call__", &Value::__call__)
            .def("__call__", &Value::__call__scale)
            .def("__call__", &Value::__call__scale_offset)
        ;
		py::def("get_osc_f_c", &get_osc_f);
		py::def("osc_value", &osc_value);
    }
}

Pineal::Pineal(int argc, char ** argv){
	this->argc = argc;
	this->argv = argv;
}

void Pineal::setup(){
	ofLog() << "Running setup()";

	try{
		Py_Initialize();
		PySys_SetArgv(argc, argv);

		PyImport_AppendInittab("core", &dsl::initcore);

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

	ofAddListener(onset.gotOnset, this, &Pineal::onsetEvent);
	ofAddListener(beat.gotBeat, this, &Pineal::beatEvent);

	ofSoundStreamSetup(nOutputs, nInputs, this);
}

void Pineal::exit(){
	ofSoundStreamStop();
	ofSoundStreamClose();
}

void Pineal::audioIn(float * input, int bufferSize, int nChannels){
	inBuf.allocate(bufferSize, nChannels);
	for(int i = 0; i < bufferSize * nChannels; i++){
		inBuf[i] = input[i];
	}

	onset.audioIn(input, bufferSize, nChannels);
	beat.audioIn(input, bufferSize, nChannels);
}

void Pineal::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);
		string address = m.getAddress();

		if(address == "/run-code"){
			ofSetColor(255);
			ofFill();
			ofSetLineWidth(1);

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
			osc_set_float(address, m.getArgAsFloat(0));
		}
	}

	sendFloat("/amp", inBuf.getRMSAmplitude());
	sendFloat("/time", ofGetElapsedTimef());
}

void Pineal::draw(){
	output.allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
	output.begin();

	ofBackground(0);

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

void Pineal::sendFloat(string name, float x){
	ofxOscMessage msg;

	msg.setAddress(name);
	msg.addFloatArg(x);
	oscServer.sendMessage(msg, false);
}

ofTexture Pineal::getTexture(){
	return output.getTexture();
}

void Pineal::onsetEvent(float & time){
	// TODO: boolean OSC
}

void Pineal::beatEvent(float & time){
	// TODO: boolean OSC
}
