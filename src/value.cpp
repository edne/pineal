#include "pineal.h"

Value::Value(){
	getter = [](){ return 0.0; };
}

Value::Value(float x){
	getter = [=](){ return x; };
}

Value::Value(function<float()> f){
	getter = f;
}

Value::Value(py::list args, int index, Value default_value){
	if(py::len(args) > index){
		py::extract<Value&> extractor(args[index]);

		if(extractor.check()){
			Value& s = extractor();
			getter = s.getter;
		}else{
			float value = py::extract<float>(args[index]);
			getter = [=](){ return value; };
		}
	}else{
		getter = default_value.getter;
	}
}

Value Value::__call__scale(float scale){
	return Value([=](){
		return getter() * scale;
	});
}

Value Value::__call__scale_offset(float scale, float offset){
	return Value([=](){
		return getter() * scale + offset;
	});
}

Value Value::__call__scale_value(Value scale){
	return Value([=](){
		return getter() * scale();
	});
}

Value Value::__call__scale_offset_value(Value scale, Value offset){
	return Value([=](){
		return getter() * scale() + offset();
	});
}

float Value::__call__(){
	return getter();
}

float Value::operator()() const{
	return getter();
}


unordered_map<string, float> float_map;

bool exists_float(string name){
	return float_map.find(name) != float_map.end();
}

void osc_set_float(string name, float x){
	float_map[name] = x;
}

float get_osc_f(string name){
	if(!exists_float(name)){
		osc_set_float(name, 0.0);
	}
	return float_map[name];
}

Value osc_value(string name){
	return Value([=](){
		if(!exists_float(name)){
			osc_set_float(name, 0.0);
		}
		return float_map[name];
	});
}

