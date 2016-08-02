#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "pineal.h"


int main(int argc, char ** argv){
	auto app = make_shared<Pineal>(argc, argv);
	auto out = make_shared<outApp>(app);

	ofGLFWWindowSettings settings;
	auto appWindow = ofCreateWindow(settings);

	settings.shareContextWith = appWindow;
	auto outWindow = ofCreateWindow(settings);

	ofRunApp(appWindow, app);
	ofRunApp(outWindow, out);
	ofRunMainLoop();
}
