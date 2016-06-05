{{ begin_module("osc") }}

	unordered_map<string, float> float_map;

	bool exists_float(string name){
		return float_map.find(name) != float_map.end();
	}

	void set_float(string name, float x){
		float_map[name] = x;
	}

	{{ module.bind("get_osc_f_c", "get_osc_f") }}
	float get_osc_f(string name, float x){
		if(!exists_float(name)){
			set_float(name, x);
		}
		return float_map[name];
	}

{{ end_module() }}
