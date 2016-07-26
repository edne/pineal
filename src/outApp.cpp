#include "outApp.h"

outApp::outApp(shared_ptr<Pineal> main){
	this->main = main;
}

void outApp::draw(){
	int w = ofGetWidth();
	int h = ofGetHeight();
	int side = max(w, h);
	main->getTexture().draw((w - side) / 2,
	                        (h - side) / 2,
	                        side, side);
}
