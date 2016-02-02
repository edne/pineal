#include "ofApp.h"
#include <boost/python.hpp>

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
        PyImport_AppendInittab( "core", &initcore );

        ns = import( "__main__" ).attr( "__dict__" );

        exec( "import hy", ns );
        exec( "from py.hy_utils import eval_hy_code", ns );
        exec( "dsl_ns = {}", ns );
        exec( "dsl_history = []", ns );

        // TODO take code from OSC
        exec( "dsl_history.append('(import [core [*]])(defn --draw-- [] (background 0.2))')", ns );
        exec( "eval_hy_code(dsl_history[-1], dsl_ns)", ns );

    } catch( error_already_set ) {
        PyErr_Print();
    }
}

//--------------------------------------------------------------
void ofApp::update(){
}

//--------------------------------------------------------------
void ofApp::draw(){
    try {
        // TODO check history
        exec( "dsl_ns['__draw__']()", ns );
    } catch( error_already_set ) {
        PyErr_Print();
    }
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
