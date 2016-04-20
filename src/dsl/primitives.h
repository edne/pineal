namespace primitives{
	PINEAL("compose_c")
	pAction compose(py::list py_actions){
		int n = 0;
		vector<pAction> actions;
		for(int i = 0; i < py::len(py_actions); i++){
			py::extract<pAction&> extractor(py_actions[i]);
			if(extractor.check()){
				n += 1;
				pAction& action = extractor();
				actions.push_back(action);
			}
		}
		return pAction([=](pEntity& e){
			for(int i = 0; i < n; i++){
				e = actions[i](e);
			}
			return e;
		});
	}

	PINEAL("change_c")
	pEntity change(pEntity& entity, py::list py_actions){
		pAction action = compose(py_actions);
		return action(entity);
	}

	PINEAL("draw")
	void draw(pEntity e){
		e();
	}

	PINEAL("group_c")
	pEntity group(py::list l){
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

		return e;
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
