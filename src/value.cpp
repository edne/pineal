#include "pineal.h"

Value::Value(){
	value = 0.0;
}

Value::Value(float x){
	value = x;
}

Value::Value(py::list args, int index, Value default_value){
	if(py::len(args) > index){
		py::extract<Value&> extractor(args[index]);

		if(extractor.check()){
			Value& s = extractor();
			value = s.value;
		}else{
			value = py::extract<float>(args[index]);
		}
	}else{
		value = default_value.value;
	}
}

float Value::operator()() const{
	return value;
}

