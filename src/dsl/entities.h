{{ begin_module("entities") }}

	unordered_map<string, ofTrueTypeFont> fonts_map;

	{{ module.bind("make_entity", "make_entity") }}
	Entity make_entity(string name, py::list args){

		if(name=="change"){
			Entity entity = py::extract<Entity>(args[0]);
			Action action = py::extract<Action>(args[1]);

			return action(entity);
		}

		if(name=="group"){
			size_t n = py::len(args);
			vector<Entity> entities;

			for(size_t i=0; i<n; i++){
				entities.push_back(py::extract<Entity>(args[i]));
			}

			Entity e([=](){
				for(size_t i=0; i<entities.size(); i++){
					entities[i]();
				}
			});

			return e;
		}

		if(name=="cube"){
			Entity e([=](){
				ofDrawBox(0.5);
			});

			return e;
		}

		if(name=="polygon"){
			int n = py::extract<int>(args[0]);

			Entity e([=](){
				ofPushMatrix();

				ofRotateZ(90);

				ofSetCircleResolution(n);
				ofDrawCircle(0, 0, 0.5);

				ofPopMatrix();
			});

			return e;
		}

		if(name=="text"){
			string font_name = py::extract<string>(args[0]);
			string s = py::extract<string>(args[1]);

			float size = 100;

			if(fonts_map.find(font_name) == fonts_map.end()){
				ofTrueTypeFont font;
				font.load(font_name, size, true, true, true);
				fonts_map[font_name] = font;
			}

			float scale = 1.0 / size;

			Entity e([=](){
				ofPushMatrix();
				ofScale(scale, scale, scale);
				fonts_map[font_name].drawStringAsShapes(s, 0, 0);
				ofPopMatrix();
			});

			return e;

		}

		return Entity();
	}

{{ end_module() }}
