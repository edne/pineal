#include "pineal.h"

Action::Action(){  // by default identity
	apply = [](Entity& e){
		return e;
	};
}

Action::Action(function<Entity(Entity&)> a){
	apply = a;
}

Entity Action::__call__(Entity& e){
	return apply(e);
}

Entity Action::operator()(Entity e) const{
	return apply(e);
}

vector<Action> cast_actions_list(py::list py_actions){
	vector<Action> actions;
	for(int i = 0; i < py::len(py_actions); i++){
		py::extract<Action&> extractor(py_actions[i]);
		if(extractor.check()){
			Action& action = extractor();
			actions.push_back(action);
		}
	}
	return actions;
}

Action fill_status(bool status){
	return Action([=](Entity& e){
		return Entity([=](){
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


Action on_camera(){
	static ofEasyCam camera;
	camera.setDistance(1);
	camera.setNearClip(0.01);

	return Action([&](Entity& e){
		return Entity([&](){
			camera.begin();
			e();
			camera.end();
		});
	});
}


Action render(Value buffer_size){
	ofFbo fbo;
	fbo.allocate(buffer_size(), buffer_size(), GL_RGBA);

	return Action([=](Entity& e){
		fbo.begin();
		glPushAttrib(GL_ALL_ATTRIB_BITS);
		glEnable(GL_BLEND);
		glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA);

		ofClear(255,255,255, 0);
		ofSetColor(255);
		ofFill();
		ofSetLineWidth(1);

		on_camera()(e)();

		glDisable(GL_BLEND);
		glPopAttrib();
		fbo.end();

		return Entity([=](){
			ofEnableAlphaBlending();
			fbo.getTexture().draw(-0.5, -0.5, 1, 1);  // TODO: side 1
			ofDisableAlphaBlending();
		});
	});
}

Action make_action(string name, py::list args){

	if(name=="compose"){
		vector<Action> actions = cast_actions_list(args);

		return Action([=](Entity& e){
			for(size_t i = 0; i < actions.size(); i++){
				e = actions[i](e);
			}
			return e;
		});
	}

	if(name=="branch"){
		vector<Action> actions = cast_actions_list(args);

		return Action([=](Entity& e){
			vector<Entity> entities;
			for(size_t i = 0; i < actions.size(); i++){
				entities.push_back(actions[i](e));
			}

			return Entity([=](){
				for(size_t i = 0; i < entities.size(); i++){
					entities[i]();
				}
			});
		});
	}

	if(name=="hide"){
		return Action([=](Entity& e){
			return Entity([=](){
			});
		});
	}

	if(name=="scale"){
		Value x(args, 0, 1.0);
		Value y(args, 1, x);
		Value z(args, 2, x);

		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofScale(x(), y(), z());
				e();
				ofPopMatrix();
			});
		});
	}

	if(name=="translate"){
		Value x(args, 0, 0.0);
		Value y(args, 1, 0.0);
		Value z(args, 2, 0.0);

		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofTranslate(x(), y(), z());
				e();
				ofPopMatrix();
			});
		});
	}

	if(name=="rotate_x"){
		Value rad(args, 0, 0.0);
		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofRotateX(180 * rad() / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	if(name=="rotate_y"){
		Value rad(args, 0, 0.0);
		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofRotateY(180 * rad() / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	if(name=="rotate_z"){
		Value rad(args, 0, 0.0);
		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofRotateZ(180 * rad() / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	if(name=="color"){
		Color p = py::extract<Color>(args[0]);
		ofColor c = p.c;

		return Action([=](Entity& e){
			return Entity([=](){
				static ofColor status_color;
				ofColor old_color = status_color;
				ofColor new_color = ofColor(c.r, c.g, c.b, c.a);

				status_color = new_color;
				ofSetColor(status_color);

				e();

				status_color = old_color;
				ofSetColor(status_color);
			});
		});
	}

	if(name=="fill"){
		return fill_status(true);
	}

	if(name=="no_fill"){
		return fill_status(false);
	}

	if(name=="line_width"){
		Value new_width(args, 0, 1.0);

		return Action([=](Entity& e){
			return Entity([=](){
				static double status_line_width = 1;
				double old_width = status_line_width;

				status_line_width = new_width();
				ofSetLineWidth(status_line_width);

				e();

				status_line_width = old_width;
				ofSetLineWidth(status_line_width);
			});
		});
	}

	if(name=="render"){
		Value buffer_size(args, 0, 1366);
		return render(buffer_size);
	}


	return Action();
}

