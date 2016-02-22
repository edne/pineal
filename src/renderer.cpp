#include "pineal.h"

Renderer::Renderer(int argc, char ** argv){
	embed = make_shared<Embed>(argc, argv);
}

void Renderer::setup(){
	ofLog() << "Running setup()";
	embed->setup();
	ofSetEscapeQuitsApp(false);
	oscReceiver.setup(7172);
}

void Renderer::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);

		if(m.getAddress() == "/code"){
			string code = m.getArgAsString(0);
			ofLog() << "OSC mesage:\n" << "/code" << "\n" << code << "\n";
			embed->update(code);
		}
	}
}

void Renderer::draw(){
	embed->draw();

	auto texture = embed->getBuffer();

	int w = ofGetWindowWidth();
	int h = ofGetWindowHeight();
	texture.draw(0, -(w - h) / 2, w, w);

	string fps = "FPS: " + ofToString(ofGetFrameRate());
	ofSetColor(255);
	ofDrawBitmapString(fps, 10, 20);

}
