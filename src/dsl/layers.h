namespace layers{
	unordered_map<string, shared_ptr<ofFbo>> layers_map;

	void new_layer(string name){
		if(layers_map.find(name) != layers_map.end()){
			return;
		}
		auto fbo = make_shared<ofFbo>();

		fbo->allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
		fbo->begin();
		ofClear(255,255,255, 0);
		fbo->end();
		layers_map[name] = fbo;
	}

    {{ bind("layers", "on_layer_c", "on_layer") }}
	void on_layer(pEntity& f, string name){
		if(layers_map.find(name) == layers_map.end()){
			new_layer(name);
		}
		ofEasyCam camera;
		camera.setDistance(1);
		camera.setNearClip(0.01);

		layers_map[name]->begin();
		camera.begin();
		f();
		camera.end();
		layers_map[name]->end();
	}

    {{ bind("layers", "layer_entity", "layer_entity") }}
	pEntity layer_entity(string name){
		return pEntity([name](){
			if(layers_map.find(name) == layers_map.end()){
				new_layer(name);
			}
			layers_map[name]->getTexture().draw(-1, -1, 2, 2);
		});
	}
}
