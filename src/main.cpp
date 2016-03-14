#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "ofApp.h"
#include "outApp.h"


int main(int argc, char ** argv){
	auto app = make_shared<ofApp>(argc, argv);
	auto out = make_shared<outApp>(app);

	ofGLFWWindowSettings settings;
	auto appWindow = ofCreateWindow(settings);

	settings.shareContextWith = appWindow;
	auto outWindow = ofCreateWindow(settings);

	ofRunApp(appWindow, app);
	ofRunApp(outWindow, out);
	ofRunMainLoop();
}
