namespace primitives{
	PINEAL("draw")
	void draw(pEntity e){
		e();
	}

	pEntity group(vector<pEntity> entities){
		pEntity e([=](){
			for(size_t i = 0; i < entities.size(); i++){
				draw(entities[i]);
			}
		});

		return e;
	}

	vector<pAction> cast_actions_list(py::list py_actions){
		vector<pAction> actions;
		for(int i = 0; i < py::len(py_actions); i++){
			py::extract<pAction&> extractor(py_actions[i]);
			if(extractor.check()){
				pAction& action = extractor();
				actions.push_back(action);
			}
		}
		return actions;
	}

	PINEAL("compose_c")
	pAction compose(py::list py_actions){
		vector<pAction> actions = cast_actions_list(py_actions);

		return pAction([=](pEntity& e){
			for(size_t i = 0; i < actions.size(); i++){
				e = actions[i](e);
			}
			return e;
		});
	}

	PINEAL("branch_c")
	pAction branch(py::list py_actions){
		vector<pAction> actions = cast_actions_list(py_actions);

		return pAction([=](pEntity& e){
			vector<pEntity> entities;
			for(size_t i = 0; i < actions.size(); i++){
				entities.push_back(actions[i](e));
			}
			return group(entities);
		});
	}

	PINEAL("change_c")
	pEntity change(pEntity& entity, py::list py_actions){
		pAction action = compose(py_actions);
		return action(entity);
	}

	PINEAL("group_c")
	pEntity group_exposed(py::list l){
		int n = py::len(l);
		vector<pEntity> entities;

		for(int i = 0; i < n; i++){
			entities.push_back(py::extract<pEntity>(l[i]));
		}

		return group(entities);
	}

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
}
