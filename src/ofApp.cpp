#include "ofApp.h"
#include <boost/python.hpp>

namespace py = boost::python;

void background(double x) {
    ofBackground(x * 255);
}

BOOST_PYTHON_MODULE(core) {
    py::def("background", &background);
}

py::object ns;

void ofApp::setup() {

    ofLog() << "Running setup()";

	oscReceiver.setup(7172);

    try {
        Py_Initialize();
        PySys_SetArgv(argc, argv);
        PyImport_AppendInittab("core", &initcore);

        ns = py::import("__main__").attr("__dict__");

        py::exec("import hy", ns);
        py::exec("from py.hy_utils import eval_hy_code", ns);
        py::exec("dsl_ns = {}", ns);
        py::exec("dsl_history = []", ns);

        // TODO take code from OSC
        py::exec("dsl_history.append('(import [core [*]])(defn --draw-- [] (background 0.2))')", ns);
        py::exec("eval_hy_code(dsl_history[-1], dsl_ns)", ns);

    } catch(py::error_already_set) {
        PyErr_Print();
    }
}

void ofApp::update() {
    while (oscReceiver.hasWaitingMessages()) {
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);

        if (m.getAddress() == "/code") {
            string code = m.getArgAsString(0);
            ofLog() << "/code " << code;
		}
    }
}

void ofApp::draw() {
    try {
        // TODO check history
        py::exec("dsl_ns['__draw__']()", ns);
    } catch (py::error_already_set) {
        PyErr_Print();
    }
}

void ofApp::keyPressed(int key) {}
void ofApp::keyReleased(int key) {}
void ofApp::mouseMoved(int x, int y) {}
void ofApp::mouseDragged(int x, int y, int button) {}
void ofApp::mousePressed(int x, int y, int button) {}
void ofApp::mouseReleased(int x, int y, int button) {}
void ofApp::mouseEntered(int x, int y) {}
void ofApp::mouseExited(int x, int y) {}
void ofApp::windowResized(int w, int h) {}
void ofApp::gotMessage(ofMessage msg) {}
void ofApp::dragEvent(ofDragInfo dragInfo) {}
