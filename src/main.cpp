#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "pineal.h"


int main(int argc, char ** argv){
	auto renderer = make_shared<Renderer>(argc, argv);

	ofGLWindowSettings settings;
	auto mainWindow = ofCreateWindow(settings);

	ofRunApp(mainWindow, renderer);
	ofRunMainLoop();
}
