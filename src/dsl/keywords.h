namespace keywords{
    {{ bind("keywords", "draw", "draw") }}
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

    {{ bind("keywords", "compose_c", "compose") }}
	pAction compose(py::list py_actions){
		vector<pAction> actions = cast_actions_list(py_actions);

		return pAction([=](pEntity& e){
			for(size_t i = 0; i < actions.size(); i++){
				e = actions[i](e);
			}
			return e;
		});
	}

    {{ bind("keywords", "branch_c", "branch") }}
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

    {{ bind("keywords", "change_c", "change") }}
	pEntity change(pEntity& entity, py::list py_actions){
		pAction action = compose(py_actions);
		return action(entity);
	}

    {{ bind("keywords", "group_c", "group_exposed") }}
	pEntity group_exposed(py::list l){
		int n = py::len(l);
		vector<pEntity> entities;

		for(int i = 0; i < n; i++){
			entities.push_back(py::extract<pEntity>(l[i]));
		}

		return group(entities);
	}
}
