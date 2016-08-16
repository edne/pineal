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
            .def("__call__", &Value::__call__scale_value)
            .def("__call__", &Value::__call__scale_offset_value)
        ;
		py::def("osc_value", &osc_value);
		py::def("make_lfo", &make_lfo);
		py::def("time_value", &time_value);
		py::def("tempo_value", &tempo_value);
    }
}

Pineal::Pineal(int argc, char ** argv){
	this->argc = argc;
	this->argv = argv;

	ofGLFWWindowSettings settings;
	mainWindow = ofCreateWindow(settings);
	// mainWindow->setVerticalSync(false);

	settings.shareContextWith = mainWindow;
	outWindow = ofCreateWindow(settings);
	ofAddListener(outWindow->events().draw, this, &Pineal::drawOut);
}


void Pineal::setup(){
	ofLog() << "Running setup()";

	Py_Initialize();
	PySys_SetArgv(argc, argv);
	PyImport_AppendInittab("core", &dsl::initcore);

	// ofSetVerticalSync(true);
	ofEnableDepthTest();
	ofEnableSmoothing();

	ofSetEscapeQuitsApp(false);

	oscReceiver.setup(7172);
	oscClient.setup("localhost", 7173);  // frontend address, TODO: read config

	ear.setup();
	code_to_entity = py::import("libs.translate").attr("Translator")();
}

void Pineal::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);
		string address = m.getAddress();

		if(address == "/run-code"){
			string code = m.getArgAsString(0);
			osc_set_string(address, code);

			try{
				drawing = code_to_entity(code);
			}catch(const py::error_already_set & e){
				PyObject *ptype, *pvalue, *ptraceback;
				PyErr_Fetch(&ptype, &pvalue, &ptraceback);
				ofLog() << PyString_AsString(pvalue);;
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
			string type = m.getArgTypeName(0);
			if(type=="f"){
				osc_set_float(address, m.getArgAsFloat(0));
			}else if(type=="s"){
				osc_set_string(address, m.getArgAsString(0));
			}
		}
	}
	ear.update();
}

void Pineal::exit(){
	ofSoundStreamStop();
	ofSoundStreamClose();
}


void draw_on_window(Entity e){
	ofBackground(0);

	int w = ofGetWidth();
	int h = ofGetHeight();
	int side = max(w, h);

	ofPushMatrix();
	ofTranslate(w/2, h/2, 0);
	ofScale(side, side, 1);
	e();
	ofPopMatrix();
}


void Pineal::draw(){
	int buffer_size = 1366;
	rendered = render(Value(buffer_size))(drawing);

	draw_on_window(rendered);

	string fps = "FPS: " + ofToString(ofGetFrameRate());
	ofSetColor(255);
	ofDrawBitmapString(fps, 10, 20);
}

void Pineal::drawOut(ofEventArgs & args){
	draw_on_window(rendered);
}

void Ear::setup(){
	oscServer.setup("localhost", 7172);

	onset.setup();
	beat.setup();

	ofAddListener(onset.gotOnset, this, &Ear::onsetEvent);
	ofAddListener(beat.gotBeat, this, &Ear::beatEvent);

	int nOutputs = 2;
	int nInputs = 2;
	ofSoundStreamSetup(nOutputs, nInputs, this);
}

void Ear::update(){
	sendFloat("/amp", inBuf.getRMSAmplitude());
	sendFloat("/time", ofGetElapsedTimef());
}

void Ear::audioIn(float * input, int bufferSize, int nChannels){
	inBuf.allocate(bufferSize, nChannels);
	for(int i = 0; i < bufferSize * nChannels; i++){
		inBuf[i] = input[i];
	}

	onset.audioIn(input, bufferSize, nChannels);
	beat.audioIn(input, bufferSize, nChannels);
	update_tempo(beat.bpm);
}

void Ear::sendFloat(string name, float x){
	ofxOscMessage msg;

	msg.setAddress(name);
	msg.addFloatArg(x);
	oscServer.sendMessage(msg, false);
}

void Ear::onsetEvent(float & time){
}

void Ear::beatEvent(float & time){
	sync_tempo();
}
