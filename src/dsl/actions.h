{{ begin_module("actions") }}

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

	{{ module.bind("make_action", "make_action") }}
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
					ofRotateY(180 * rad() / PI);
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

		return Action();
	}

{{ end_module() }}
