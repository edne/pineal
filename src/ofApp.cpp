#include "ofApp.h"
#include <boost/python.hpp>


namespace dsl {
    namespace py = boost::python;

    void background(double x) {
        ofBackground(x * 255);
    }

    BOOST_PYTHON_MODULE(core) {
        py::def("background", &background);
    }

    py::dict ns;
    py::object eval_hy_code;
    py::list history;

    void setup(int argc, char **argv) {
        try {
            Py_Initialize();
            PySys_SetArgv(argc, argv);
            PyImport_AppendInittab("core", &initcore);

            py::import("hy");
            eval_hy_code = py::import("py.hy_utils").attr("eval_hy_code");

            history.append("(import [core [*]])(defn --draw-- [] (background 0.2))");
            eval_hy_code(history.pop(), ns);

        } catch (py::error_already_set) {
            PyErr_Print();
        }
    }

    void draw() {
        try {
            eval_hy_code("(--draw--)", ns);
        } catch (py::error_already_set) {
            PyErr_Print();
        }
    }
}

void ofApp::setup() {
    ofLog() << "Running setup()";
	oscReceiver.setup(7172);
    dsl::setup(argc, argv);
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
    dsl::draw();
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
