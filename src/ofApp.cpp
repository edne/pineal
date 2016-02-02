#include "ofApp.h"
#include <boost/python.hpp>

#if PY_VERSION_HEX >= 0x03000000
#  define MODULE_INIT_FN(name) BOOST_PP_CAT(PyInit_, name)
#  define PYTHON_BUILTINS "builtins"
#else
#  define MODULE_INIT_FN(name) BOOST_PP_CAT(init, name)
#  define PYTHON_BUILTINS "__builtin__"
#endif

using namespace boost::python;

void background(double x){
    ofBackground( x * 255 );
}

BOOST_PYTHON_MODULE(core)
{
    def( "background", &background );
}

object ns;

//--------------------------------------------------------------
void ofApp::setup(){

    ofLog() << "Running setup()";

    try {
        Py_Initialize();
        PySys_SetArgv( argc, argv );

        ns = import( "__main__" ).attr( "__dict__" );

        ns["__builtins__"] = import( PYTHON_BUILTINS );
        PyImport_AppendInittab("core", &initcore);

        exec( "from py.visions import load", ns );
        exec( "vision = load('data/test.pn')", ns );

    } catch( error_already_set ) {
        PyErr_Print();
    }
}

//--------------------------------------------------------------
void ofApp::update(){
    exec( "vision.loop()", ns );
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
void ofApp::mouseMoved(int x, int y){

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
