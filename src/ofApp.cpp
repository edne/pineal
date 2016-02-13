#include "ofApp.h"
#include <boost/python.hpp>


namespace dsl{
	namespace py = boost::python;

    void log(string s){
        ofLog() << s;
    }

	void background(double r, double g, double b){
		ofBackground(r * 255, g * 255, b * 255);
	}

	BOOST_PYTHON_MODULE(core){
		py::def("log", &log);
		py::def("background", &background);
	}

    py::object vision;

	void setup(int argc, char ** argv){
		try{
			Py_Initialize();
			PySys_SetArgv(argc, argv);
			PyImport_AppendInittab("core", &initcore);

			py::import("hy");
            vision = py::import("py.vision").attr("Vision")();

		}catch(py::error_already_set){
			PyErr_Print();
		}
	}

	void update(string code){
		try{
            ofLog() << "Updating:\n" << code << "\n";
            vision.attr("update")(code);
		}catch(py::error_already_set){
			PyErr_Print();
		}
	}

	void draw(){
		try{
            vision.attr("draw")();
            ofDrawBitmapString("FPS: " + ofToString(ofGetFrameRate()), 10, 20);
		}catch(py::error_already_set){
			PyErr_Print();
		}
	}
}

void ofApp::setup(){
	ofLog() << "Running setup()";
	oscReceiver.setup(7172);
	dsl::setup(argc, argv);
}

void ofApp::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);

		if(m.getAddress() == "/code"){
			string code = m.getArgAsString(0);
			ofLog() << "OSC mesage:\n" << "/code" << "\n" << code << "\n";
			dsl::update(code);
		}
	}
}

void ofApp::draw(){
	dsl::draw();
}

void ofApp::keyPressed(int key){}
void ofApp::keyReleased(int key){}
void ofApp::mouseMoved(int x, int y){}
void ofApp::mouseDragged(int x, int y, int button){}
void ofApp::mousePressed(int x, int y, int button){}
void ofApp::mouseReleased(int x, int y, int button){}
void ofApp::mouseEntered(int x, int y){}
void ofApp::mouseExited(int x, int y){}
void ofApp::windowResized(int w, int h){}
void ofApp::gotMessage(ofMessage msg){}
void ofApp::dragEvent(ofDragInfo dragInfo){}
