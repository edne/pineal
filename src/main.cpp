#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "ofApp.h"


int main(int argc, char ** argv){
	auto app = make_shared<ofApp>(argc, argv);

	ofGLWindowSettings settings;
	auto mainWindow = ofCreateWindow(settings);

	ofRunApp(mainWindow, app);
	ofRunMainLoop();
}
