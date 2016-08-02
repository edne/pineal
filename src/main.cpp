#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "pineal.h"


int main(int argc, char ** argv){
	shared_ptr<Pineal> app = make_shared<Pineal>(argc, argv);
	shared_ptr<outApp> out = make_shared<outApp>(app);

	ofGLFWWindowSettings settings;
	shared_ptr<ofAppBaseWindow> appWindow = ofCreateWindow(settings);

	settings.shareContextWith = appWindow;
	shared_ptr<ofAppBaseWindow> outWindow = ofCreateWindow(settings);

	ofRunApp(appWindow, app);
	ofRunApp(outWindow, out);
	ofRunMainLoop();
}
