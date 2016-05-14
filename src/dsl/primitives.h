{{ begin_module("primitives") }}

	{{ module.bind("cube", "cube") }}
	pEntity cube(){
		pEntity e([=](){
			ofDrawBox(0.5);
		});

		return e;
	}

	{{ module.bind("polygon", "polygon") }}
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
	unordered_map<string, ofTrueTypeFont> fonts_map;

	{{ module.bind("text_c", "text") }}
	pEntity text(string font_name, string s){
		float size = 100;

		if(fonts_map.find(font_name) == fonts_map.end()){
			ofTrueTypeFont font;
			font.load(font_name, size, true, true, true);
			fonts_map[font_name] = font;
		}

		float scale = 1.0 / size;

		pEntity e([=](){
			ofPushMatrix();
			ofScale(scale, scale, scale);
			fonts_map[font_name].drawStringAsShapes(s, 0, 0);
			ofPopMatrix();
		});

		return e;
	}

{{ end_module() }}
