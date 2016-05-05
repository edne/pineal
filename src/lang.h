#pragma once

#include <boost/python.hpp>
namespace py = boost::python;


class pEntity{
	public:
		pEntity(){
			draw = [](){};
		}

		pEntity(py::object f){
			draw = [=](){ f(); };
		}

		pEntity(function<void(void)> f){
			draw = f;
		}

		void operator()() const{
			draw();
		}

	private:
		function<void(void)> draw;
};

class pAction{
	public:
		pAction(){  // by default identity
			apply = [](pEntity& e){
				return e;
			};
		}

		pAction(function<pEntity(pEntity&)> a){
			apply = a;
		}

		pEntity __call__(pEntity& e){
			return apply(e);
		}

		pEntity operator()(pEntity e) const{
			return apply(e);
		}

	private:
		function<pEntity(pEntity&)> apply;
};

class pValue{
	public:
		pValue(){
			value = 0.0;
		}

		pValue(float x){
			value = x;
		}

		pValue(py::list args, int index, float default_value) :
			pValue(args, index, pValue(default_value)){
		}

		pValue(py::list args, int index, pValue default_value){
			if(py::len(args) > index){
				py::extract<pValue&> extractor(args[index]);

				if(extractor.check()){
					pValue& s = extractor();
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

class pColor{
	public:
		pColor(){
		}

		pColor(ofColor _c){
			c = _c;
		}

		// TODO: constructor with ofColor
		ofColor c;
};
