namespace osc{
	unordered_map<string, float> values_map;

	bool exists_value(string name){
		return values_map.find(name) != values_map.end();
	}

	void set_value(string name, float x){
		values_map[name] = x;
	}

	PINEAL("osc_value")
	float get_value_with_default(string name, float x){
		if(!exists_value(name)){
			set_value(name, x);
		}
		return values_map[name];
	}

	PINEAL("osc_value")
	float get_value(string name){
		return get_value_with_default(name, 0.0);
	}
}
