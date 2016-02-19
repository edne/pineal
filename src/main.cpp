#include "ofMain.h"
#include "ofApp.h"
#include "ofAppGLFWWindow.h"


int main(int argc, char ** argv){
	auto mainApp = make_shared<ofApp>();
	mainApp->argc = argc;
	mainApp->argv = argv;

	ofGLWindowSettings settings;
	auto mainWindow = ofCreateWindow(settings);

	ofRunApp(mainWindow, mainApp);
	ofRunMainLoop();
}
