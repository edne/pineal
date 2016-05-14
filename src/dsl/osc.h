namespace osc{
	unordered_map<string, float> values_map;

	bool exists_value(string name){
		return values_map.find(name) != values_map.end();
	}

	void set_value(string name, float x){
		values_map[name] = x;
	}

    {{ bind("osc", "get_osc_f_c", "get_osc_f_with_default") }}
	float get_osc_f_with_default(string name, float x){
		if(!exists_value(name)){
			set_value(name, x);
		}
		return values_map[name];
	}

    {{ bind("osc", "get_osc_f_c", "get_osc_f") }}
	float get_osc_f(string name){
		return get_osc_f_with_default(name, 0.0);
	}
}
