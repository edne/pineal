#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "pineal.h"


int main(int argc, char ** argv){
	shared_ptr<Pineal> pineal = make_shared<Pineal>(argc, argv);
	ofRunApp(pineal->mainWindow, pineal);

	ofRunMainLoop();
}
