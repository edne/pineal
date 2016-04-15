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
		// at pAction / pEntity creation time
		pValue(){
			is_literal = true;
			value = 0.0;
		}

		pValue(float x){
			is_literal = true;
			value = x;
		}

		pValue(string k){
			is_literal = false;
			key = k;
		}

		pValue(py::list args, int index, float default_value) :
			pValue(args, index, pValue(default_value)){
		}

		pValue(py::list args, int index, pValue default_value){
			if(py::len(args) > index){
				py::extract<pValue&> extractor(args[index]);

				if(extractor.check()){
					pValue& s = extractor();
					is_literal = s.is_literal;
					key = s.key;
					value = s.value;
				}else{
					is_literal = true;
					value = py::extract<float>(args[index]);
				}
			}else{
				is_literal = default_value.is_literal;
				value = default_value.value;
				key = default_value.key;
			}
		}
		//

		// at drawing time, from the pEntity that use the value
		float operator()() const{
			if(is_literal){
				return value;
			}else{
				if(symbol_table.find(key) != symbol_table.end()){
					return symbol_table[key].top();
				}else{
					// TODO: raise a Python exception
					ofLog() << "Using unbound symbol";
					return 0.0;
				}
			}
		}
		//

		// at drawing time, from the pEntity that assign values
		static void define_symbol(string key){
			if(symbol_table.find(key) != symbol_table.end()){
				symbol_table[key] = stack<float>();
			}
			symbol_table[key].push(0.0);
		}

		static void remove_symbol(string key){
			symbol_table[key].pop();
			if(symbol_table[key].empty()){
				symbol_table.erase(key);
			}
		}

		static void update_value(string key, float x){
			symbol_table[key].top() = x;
		}
		//

    private:
		static unordered_map<string, stack<float>> symbol_table;
		bool is_literal;
		float value;
		string key;
};
