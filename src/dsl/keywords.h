{{ begin_module("keywords") }}

	{{ module.bind("draw", "draw") }}
	void draw(Entity e){
		e();
	}

	Entity group(vector<Entity> entities){
		Entity e([=](){
			for(size_t i = 0; i < entities.size(); i++){
				draw(entities[i]);
			}
		});

		return e;
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

	{{ module.bind("compose_c", "compose") }}
	Action compose(py::list py_actions){
		vector<Action> actions = cast_actions_list(py_actions);

		return Action([=](Entity& e){
			for(size_t i = 0; i < actions.size(); i++){
				e = actions[i](e);
			}
			return e;
		});
	}

	{{ module.bind("branch_c", "branch") }}
	Action branch(py::list py_actions){
		vector<Action> actions = cast_actions_list(py_actions);

		return Action([=](Entity& e){
			vector<Entity> entities;
			for(size_t i = 0; i < actions.size(); i++){
				entities.push_back(actions[i](e));
			}
			return group(entities);
		});
	}

	{{ module.bind("change_c", "change") }}
	Entity change(Entity& entity, py::list py_actions){
		Action action = compose(py_actions);
		return action(entity);
	}

	{{ module.bind("group_c", "group_exposed") }}
	Entity group_exposed(py::list l){
		int n = py::len(l);
		vector<Entity> entities;

		for(int i = 0; i < n; i++){
			entities.push_back(py::extract<Entity>(l[i]));
		}

		return group(entities);
	}

{{ end_module() }}
