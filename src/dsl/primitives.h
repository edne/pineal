namespace primitives{
	PINEAL("cube")
	pEntity cube(){
		pEntity e([=](){
			ofDrawBox(0.5);
		});

		return e;
	}

	PINEAL("polygon")
	pEntity polygon(float n){
		pEntity e([=](){
			ofPushMatrix();

			ofRotateZ(90);

			ofSetCircleResolution(n);
			ofDrawCircle(0, 0, 1);

			ofPopMatrix();
		});

		return e;
	}


	// TODO font memoizing
	ofTrueTypeFont font;

	void font_setup(string font_name){
		font.load(font_name, 100, true, true, true);
	}

	PINEAL("text")
	pEntity text(string s){
		pEntity e([=](){
			ofPushMatrix();
			ofScale(0.01, 0.01, 0.01);
			font.drawStringAsShapes(s, - 50, - 50);
			ofPopMatrix();
		});

		return e;
	}
}
