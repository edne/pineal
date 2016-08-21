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
unordered_map<string, string> string_map;

bool exists_float(string name){
	return float_map.find(name) != float_map.end();
}

void osc_set_float(string name, float x){
	float_map[name] = x;
}

bool exists_string(string name){
	return string_map.find(name) != string_map.end();
}

void osc_set_string(string name, string x){
	string_map[name] = x;
}

string osc_get_string(string name){
	if(!exists_string(name)){
		osc_set_string(name, "");
	}
	return string_map[name];
}

Value osc_value(string name, py::list args){
	Value scale(args, 0, 1.0);
	Value offset(args, 1, 0.0);

	return Value([=](){
		if(!exists_float(name)){
			osc_set_float(name, 0.0);
		}
		return float_map[name] * scale() + offset();
	});
}

float tempo = 0.0;
float t0 = ofGetElapsedTimef();

void update_tempo(float bpm){
	float t1 = ofGetElapsedTimef();
	float dt = t1 - t0;
	t0 = t1;

	//ofLog() << bpm;
	if(bpm > 0){
		tempo += dt * bpm / 60;
	}else{
	}
}

void sync_tempo(){
	float weigth = 0.25;
	float frac = fmod(tempo, 1.0);

	//ofLog() << tempo;
	if(frac < 0.5){
		tempo = floor(tempo) + frac*weigth;
	}else{
		tempo = floor(tempo) + 1.0 - frac*weigth;
	}
}

Value time_value(){
	return Value([=](){
		return ofGetElapsedTimef();
	});
}

Value tempo_value(){
	return Value([=](){
		return tempo;
	});
}

Value make_lfo(string name, py::list args){
	Value t(args, 0, time_value());

	if(name == "sin"){
		Value freq  (args, 1, 1.0);
		Value amp   (args, 2, 0.5);
		Value offset(args, 3, 0.5);
		Value phase (args, 4, 0.0);

		return Value([=](){
			return sin(t()*2*PI * freq() + phase()*2*PI) * amp() + offset();
		});
	}

	if(name == "saw"){
		Value freq  (args, 1, 1.0);
		Value amp   (args, 2, 0.5);
		Value offset(args, 3, 0.5);
		Value phase (args, 4, 0.0);

		return Value([=](){
			return (fmod(t() * freq() + phase(), 1) - 0.5) * 2 * amp() + offset();
		});
	}

	if(name == "pwm"){
		Value pwm   (args, 1, 0.5);
		Value freq  (args, 2, 1.0);
		Value amp   (args, 3, 0.5);
		Value offset(args, 4, 0.5);
		Value phase (args, 5, 0.0);

		return Value([=](){
			if(fmod(t() * freq() + phase(), 1) > pwm()){
				return amp() + offset();
			}
			return -amp() + offset();
		});
	}

	return Value(0);
}
