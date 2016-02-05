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

	py::object evalHyCode;
	py::object hyDraw;
	list<string> history;

	void logError(){
		PyObject * ptype, * pvalue, * ptraceback;
		PyErr_Fetch(&ptype, &pvalue, &ptraceback);
		string errorMessage = PyString_AsString(pvalue);

		ofLog() << "Error:\n" << errorMessage << "\n";  // TODO: change error level
		// PyErr_Print();
	}

	void handleError(){
		logError();
		ofLog() << "Popping away:\n" << history.back() << "\n";
		history.pop_back();  // the broken one

		if(history.empty()){
			update("");
		}else{
			string code = history.back();
			history.pop_back();  // the good one
			update(code);
		}
	}

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
		ofLog() << "Updating:\n" << code << "\n";

		history.push_back(code);
		try{
			py::dict nameSpace;  // do I really need a "global" namespace?
			hyDraw = evalHyCode("(import [core [*]])(defn --draw-- []"
					            + history.back() + ") --draw--",
					            nameSpace);
		}catch(py::error_already_set){
			handleError();
		}
	}

	void draw(){
		try{
			hyDraw();
		}catch(py::error_already_set){
			handleError();
		}

		stringstream text;
		text << "FPS: " << ofToString(ofGetFrameRate()) << "\n\n";
		text << history.back();
		ofDrawBitmapString(text.str().c_str(), 10, 20);
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
