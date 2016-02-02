#include "ofApp.h"
#include <boost/python.hpp>

//--------------------------------------------------------------
void ofApp::setup(){
    using namespace boost::python;

    ofLog() << "setup";

    try {
        Py_Initialize();

        object main_module((
             handle<>(borrowed(PyImport_AddModule("__main__")))));

        object main_namespace = main_module.attr("__dict__");

        handle<> ignored(( PyRun_String( "print \"Running Python\"",
                                         Py_file_input,
                                         main_namespace.ptr(),
                                         main_namespace.ptr() ) ));
    } catch( error_already_set ) {
        PyErr_Print();
    }
}

//--------------------------------------------------------------
void ofApp::update(){

}

//--------------------------------------------------------------
void ofApp::draw(){

}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
