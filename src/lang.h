#pragma once

#include <boost/python.hpp>
namespace py = boost::python;


class Entity{
	public:
		Entity(){
			draw = [](){};
		}

		Entity(py::object f){
			draw = [=](){ f(); };
		}

		Entity(function<void(void)> f){
			draw = f;
		}

		void operator()() const{
			draw();
		}

	private:
		function<void(void)> draw;
};

class Action{
	public:
		Action(){  // by default identity
			apply = [](Entity& e){
				return e;
			};
		}

		Action(function<Entity(Entity&)> a){
			apply = a;
		}

		Entity __call__(Entity& e){
			return apply(e);
		}

		Entity operator()(Entity e) const{
			return apply(e);
		}

	private:
		function<Entity(Entity&)> apply;
};

class Value{
	public:
		Value(){
			value = 0.0;
		}

		Value(float x){
			value = x;
		}

		Value(py::list args, int index, float default_value) :
			Value(args, index, Value(default_value)){
		}

		Value(py::list args, int index, Value default_value){
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

		float operator()() const{
			return value;
		}

    private:
		float value;
};

class Color{
	public:
		Color(){
		}

		Color(ofColor _c){
			c = _c;
		}

		// TODO: constructor with ofColor
		ofColor c;
};
