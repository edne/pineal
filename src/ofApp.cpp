#include "ofApp.h"

void ofApp::setup(){
	ofLog() << "Running setup()";
	ofSetEscapeQuitsApp(false);
	oscReceiver.setup(7172);
	embed = pnEmbed();
	embed.setup(ofGetScreenWidth(), argc, argv);
}

void ofApp::update(){
	while(oscReceiver.hasWaitingMessages()){
		// get the next message
		ofxOscMessage m;
		oscReceiver.getNextMessage(m);

		if(m.getAddress() == "/code"){
			string code = m.getArgAsString(0);
			ofLog() << "OSC mesage:\n" << "/code" << "\n" << code << "\n";
			embed.update(code);
		}
	}
}

void ofApp::draw(){
	embed.draw();

	ofFbo fbo = embed.getBuffer();

	int w = ofGetWindowWidth();
	int h = ofGetWindowHeight();
	fbo.draw(0, -(w - h) / 2, w, w);

	string fps = "FPS: " + ofToString(ofGetFrameRate());
	ofSetColor(255);
	ofDrawBitmapString(fps, 10, 20);

}

void ofApp::keyPressed(int key){}
void ofApp::keyReleased(int key){}
void ofApp::mouseMoved(int x, int y){}
void ofApp::mouseDragged(int x, int y, int button){}
void ofApp::mousePressed(int x, int y, int button){}
void ofApp::mouseReleased(int x, int y, int button){}
void ofApp::mouseEntered(int x, int y){}
void ofApp::mouseExited(int x, int y){}
void ofApp::windowResized(int w, int h){}
void ofApp::gotMessage(ofMessage msg){}
void ofApp::dragEvent(ofDragInfo dragInfo){}
