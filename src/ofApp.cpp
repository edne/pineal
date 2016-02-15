#include "ofApp.h"
#include <boost/python.hpp>


namespace dsl{
	namespace py = boost::python;

	void of_log(string s){
		ofLog() << s;
	}

	void background(double r, double g, double b){
		ofBackground(r * 255, g * 255, b * 255);
	}

	void cube(double r){
		ofDrawBox(r);
	}

	void scale(py::object f, double r){
		ofPushMatrix();
		ofScale(r, r, r);
		f();
		ofPopMatrix();
	}

	ofColor status_color;
	void color(py::object f, double r, double g, double b){
		ofColor old_color = status_color;
		ofColor new_color = ofColor(r * 255, g * 255, b * 255);

		status_color = new_color;
		ofSetColor(status_color);

		f();

		status_color = old_color;
		ofSetColor(status_color);
	}

	bool status_fill = true;
	void _fill(py::object f, bool status){
		bool old_fill = status_fill;
		bool new_fill = status;

		status_fill = new_fill;
		if(status_fill){
			ofFill();
		}else{
			ofNoFill();
		}

		f();

		status_fill = old_fill;
		if(status_fill){
			ofFill();
		}else{
			ofNoFill();
		}
	}

	void fill(py::object f){
		_fill(f, true);
	}

	void no_fill(py::object f){
		_fill(f, false);
	}

	BOOST_PYTHON_MODULE(core){
		py::def("of_log", &of_log);
		py::def("background", &background);
		py::def("cube", &cube);
		py::def("scale", &scale);
		py::def("color", &color);
		py::def("fill", &fill);
		py::def("no_fill", &no_fill);
	}

	py::object vision;
	ofEasyCam camera;

	void setup(int argc, char ** argv){
		try{
			Py_Initialize();
			PySys_SetArgv(argc, argv);
			PyImport_AppendInittab("core", &initcore);

			vision = py::import("py.vision").attr("Vision")();

			ofSetVerticalSync(true);
			ofEnableDepthTest();

			camera.setDistance(1);
			camera.setNearClip(0.01);

			ofSetColor(255);
			ofFill();
			ofSetLineWidth(1);

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
			camera.begin();
			vision.attr("draw")();
			camera.end();

			string fps = "FPS: " + ofToString(ofGetFrameRate());
			ofSetColor(255);
			ofDrawBitmapString(fps, 10, 20);
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
