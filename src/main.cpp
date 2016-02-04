#include "ofMain.h"
#include "ofApp.h"

int main(int argc, char ** argv){
	ofSetupOpenGL(1024, 768, OF_WINDOW);

	ofApp * app = new ofApp();
	app->argc = argc;
	app->argv = argv;

	ofRunApp(app);
}
