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
		pValue r(args, 0, 0.5);

		pEntity e([=](){
			ofDrawBox(r());
		});

		if(py::len(actions) > 0){
			e = change(e, actions);
		}

		return e;
	}

	PINEAL("polygon")
	pEntity polygon(py::list args, py::list actions){
		pValue n(args, 0, 4);
		pValue r(args, 1, 0.5);

		pEntity e([=](){
			ofPushMatrix();

			ofScale(r(), r(), r());
			ofRotateZ(90);

			ofSetCircleResolution(n());
			ofDrawCircle(0, 0, 1);

			ofPopMatrix();
		});

		if(py::len(actions) > 0){
			e = change(e, actions);
		}

		return e;
	}
}
