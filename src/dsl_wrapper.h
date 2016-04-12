// DO NOT EDIT THIS FILE
// generated using scripts/generate.hy and code in src/dsl/

#pragma once
#define PINEAL(_)

namespace dsl{
	namespace transformations{
		PINEAL("scale")
		pAction scale_xyz(double x, double y, double z){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					ofPushMatrix();
					ofScale(x, y, z);
					e();
					ofPopMatrix();
				});
			});
		}

		PINEAL("translate")
		pAction translate_xyz(double x, double y, double z){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					ofPushMatrix();
					ofTranslate(x, y, z);
					e();
					ofPopMatrix();
				});
			});
		}

		PINEAL("rotate_x")
		pAction rotate_x(double rad){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					ofPushMatrix();
					ofRotateX(180 * rad / PI);
					e();
					ofPopMatrix();
				});
			});
		}

		PINEAL("rotate_y")
		pAction rotate_y(double rad){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					ofPushMatrix();
					ofRotateY(180 * rad / PI);
					e();
					ofPopMatrix();
				});
			});
		}

		PINEAL("rotate_z")
		pAction rotate_z(double rad){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					ofPushMatrix();
					ofRotateZ(180 * rad / PI);
					e();
					ofPopMatrix();
				});
			});
		}

		typedef enum{
			X, Y, Z
		}Axis;

		pAction turn(Axis axis, int n){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					double rot;

					ofPushMatrix();
					for(int i=0; i<n; i++){
						e();
						rot = 360.0 / n;
						if(axis == X){
							ofRotateX(rot);
						}else if(axis == Y){
							ofRotateY(rot);
						}else if(axis == Z){
							ofRotateZ(rot);
						}
					}
					ofPopMatrix();
				});
			});
		}

		PINEAL("turn_x")
		pAction turn_x(int n){
			return turn(X, n);
		}

		PINEAL("turn_y")
		pAction turn_y(int n){
			return turn(Y, n);
		}

		PINEAL("turn_z")
		pAction turn_z(int n){
			return turn(Z, n);
		}
	}

	namespace audio{
		bool beat_value = false;
		int beat_count = 0;
		float beat_time = 1.0;
		float last_beat = 0;

		bool onset_value = false;
		float last_onset = 0;

		ofSoundBuffer inBuf;


		void update(){
			beat_value = false;
			onset_value = false;
		}

		void set_inBuf(ofSoundBuffer in){
			inBuf = in;
		}

		void set_beat(){
			beat_value = true;
			beat_count += 1;

			float actual_time = (float)ofGetSystemTimeMicros() / 1000;
			beat_time = actual_time - last_beat;
			last_beat = actual_time;
		}

		void set_onset(){
			onset_value = true;

			float actual_time = (float)ofGetSystemTimeMicros() / 1000;
			last_onset = actual_time;
		}

		bool beat(int n, float t, int position){
			float actual_time = (float)ofGetSystemTimeMicros() / 1000;

			if(beat_count % n == position && actual_time - last_beat < beat_time * t){
				return true;
			}else{
				return false;
			}
		}

		bool onset(float t){
			float actual_time = (float)ofGetSystemTimeMicros() / 1000;

			if(actual_time - last_onset < beat_time * t){
				return true;
			}else{
				return false;
			}
		}

		PINEAL("rms")
		float rms(){
			return inBuf.getRMSAmplitude();
		}

		PINEAL("at_event")
		pAction at_event(bool event){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					if(event){
		                e();
		            }
				});
			});
		}

		PINEAL("at_beat")
		pAction at_beat(int n, float t, int position){
			return at_event(beat(n, t, position));
		}

		PINEAL("at_onset")
		pAction at_onset(int n, float t, int position){
			return at_event(onset(t));
		}
	}

	namespace primitives{
		pEntity change(pEntity& entity, py::list actions){
			for(int i = 0; i < py::len(actions); i++){
				py::extract<pAction&> extractor(actions[i]);
				if(extractor.check()){
					pAction& action = extractor();
					entity = action(entity);
				}
			}
			return entity;
		}

		PINEAL("draw")
		void draw(pEntity e){
			e();
		}

		PINEAL("group")
		pEntity group(py::list l, py::list actions){
			int n = py::len(l);
			vector<pEntity> v;

			for(int i = 0; i < n; i++){
				v.push_back(py::extract<pEntity>(l[i]));
			}

			pEntity e([n, v](){
				for(int i = 0; i < n; i++){
					draw(v[i]);
				}
			});

			if(py::len(actions) > 0){
				e = change(e, actions);
			}

			return e;
		}

		PINEAL("cube")
		pEntity cube(py::list args, py::list actions){
			float r;

			if(py::len(args) > 0){
				r = py::extract<float>(args[0]);
			}else{
				r = 0.5;
			}

			pEntity e([=](){
				ofDrawBox(r);
			});

			if(py::len(actions) > 0){
				e = change(e, actions);
			}

			return e;
		}

		PINEAL("polygon")
		pEntity polygon(py::list args, py::list actions){
			int n;
			float r;

			if(py::len(args) > 0){
				n = py::extract<int>(args[0]);
			}else{
				// TODO: Raise Python exception
				return pEntity();
			}

			if(py::len(args) > 1){
				r = py::extract<float>(args[1]);
			}else{
				r = 0.5;
			}

			pEntity e([=](){
				ofPushMatrix();

				ofScale(r, r, r);
				ofRotateZ(90);

				ofSetCircleResolution(n);
				ofDrawCircle(0, 0, 1);

				ofPopMatrix();
			});

			if(py::len(actions) > 0){
				e = change(e, actions);
			}

			return e;
		}
	}

	namespace osc{
		unordered_map<string, float> values_map;

		bool exists_value(string name){
			return values_map.find(name) != values_map.end();
		}

		void set_value(string name, float x){
			values_map[name] = x;
		}

		PINEAL("osc_value")
		float get_value_with_default(string name, float x){
			if(!exists_value(name)){
				set_value(name, x);
			}
			return values_map[name];
		}

		PINEAL("osc_value")
		float get_value(string name){
			return get_value_with_default(name, 0.0);
		}

	}

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

		PINEAL("on_layer_c")
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

		PINEAL("layer_entity")
		pEntity layer_entity(string name){
			return pEntity([name](){
				if(layers_map.find(name) == layers_map.end()){
					new_layer(name);
				}
				layers_map[name]->getTexture().draw(-1, -1, 2, 2);
			});
		}
	}

	namespace colors{
		void setup(){
			ofSetColor(255);
			ofFill();
			ofSetLineWidth(1);
		}

		PINEAL("background")
		void background(double r, double g, double b, double a){
			ofBackground(r * 255, g * 255, b * 255, a * 255);
		}

		PINEAL("color")
		pAction color(double r, double g, double b, double a){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					static ofColor status_color;
					ofColor old_color = status_color;
					ofColor new_color = ofColor(r * 255, g * 255, b * 255, a * 255);

					status_color = new_color;
					ofSetColor(status_color);

					e();

					status_color = old_color;
					ofSetColor(status_color);
				});
			});
		}

		pAction fill_status(bool status){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					static bool status_fill = true;
					bool old_fill = status_fill;
					bool new_fill = status;

					status_fill = new_fill;
					if(status_fill){
						ofFill();
					}else{
						ofNoFill();
					}

					e();

					status_fill = old_fill;
					if(status_fill){
						ofFill();
					}else{
						ofNoFill();
					}
				});
			});
		}

		PINEAL("fill")
		pAction fill(){
			return fill_status(true);
		}

		PINEAL("no_fill")
		pAction no_fill(){
			return fill_status(false);
		}

		PINEAL("line_width")
		pAction line_width(double new_width){
			return pAction([=](pEntity& e){
				return pEntity([=](){
					static double status_line_width = 1;
					double old_width = status_line_width;

					status_line_width = new_width;
					ofSetLineWidth(status_line_width);

					e();

					status_line_width = old_width;
					ofSetLineWidth(status_line_width);
				});
			});
		}
	}

	BOOST_PYTHON_MODULE(core){
		py::class_<pEntity>("pEntity")
		    .def(py::init<py::object>())
		;

		py::class_<pAction>("pAction")
		    .def("__call__", &pAction::__call__)
		;

		py::def("scale", &transformations::scale_xyz);
		py::def("translate", &transformations::translate_xyz);
		py::def("rotate_x", &transformations::rotate_x);
		py::def("rotate_y", &transformations::rotate_y);
		py::def("rotate_z", &transformations::rotate_z);
		py::def("turn_x", &transformations::turn_x);
		py::def("turn_y", &transformations::turn_y);
		py::def("turn_z", &transformations::turn_z);

		py::def("rms", &audio::rms);
		py::def("at_event", &audio::at_event);
		py::def("at_beat", &audio::at_beat);
		py::def("at_onset", &audio::at_onset);

		py::def("draw", &primitives::draw);
		py::def("group", &primitives::group);
		py::def("cube", &primitives::cube);
		py::def("polygon", &primitives::polygon);

		py::def("osc_value", &osc::get_value_with_default);
		py::def("osc_value", &osc::get_value);

		py::def("on_layer_c", &layers::on_layer);
		py::def("layer_entity", &layers::layer_entity);

		py::def("background", &colors::background);
		py::def("color", &colors::color);
		py::def("fill", &colors::fill);
		py::def("no_fill", &colors::no_fill);
		py::def("line_width", &colors::line_width);}
}