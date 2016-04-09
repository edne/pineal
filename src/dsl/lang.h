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

	return pEntity([n, v](){
		for(int i = 0; i < n; i++){
			draw(v[i]);
		}
	});
}

PINEAL("change_c")
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
