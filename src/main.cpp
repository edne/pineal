#include "ofMain.h"
#include "ofAppGLFWWindow.h"
#include "pineal.h"


int main(int argc, char ** argv){
	shared_ptr<Pineal> pineal = make_shared<Pineal>(argc, argv);
	ofRunApp(pineal->ofWindow, pineal);

	shared_ptr<View> out = make_shared<View>(pineal);
	ofRunApp(out->ofWindow, out);

	ofRunMainLoop();
}
