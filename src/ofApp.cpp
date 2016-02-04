#include "ofApp.h"
#include <boost/python.hpp>


namespace dsl{
	namespace py = boost::python;

	void background(double x){
		ofBackground(x * 255);
	}

	BOOST_PYTHON_MODULE(core){
		py::def("background", &background);
	}

	py::dict nameSpace;
	py::object evalHyCode;
	// py::list history;  // TODO: replace it with a vector

	void setup(int argc, char ** argv){
		try{
			Py_Initialize();
			PySys_SetArgv(argc, argv);
			PyImport_AppendInittab("core", &initcore);

			py::import("hy");
			evalHyCode = py::import("py.hy_utils").attr("eval_hy_code");

			update("");

		}catch(py::error_already_set){
			PyErr_Print();
		}
	}

	void update(string code){
		ofLog() << "dsl: update";
		ofLog() << code;
		code = "(import [core [*]])(defn --draw-- [] " + code + ")";
		ofLog() << code;

		try{
			evalHyCode(code, nameSpace);
		}catch(py::error_already_set){
			PyErr_Print();
		}
		// history.append(code);
	}

	void draw(){
		try{
			evalHyCode("(--draw--)", nameSpace);
		}catch(py::error_already_set){
			PyErr_Print();

			// history.pop();  // the broken one
			// string code = history.pop();
			// update(code);
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
			ofLog() << "ofApp" << "/code " << code;
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
