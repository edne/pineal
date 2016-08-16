#include "pineal.h"


Color::Color(){
	get_ofColor = [=](){
		ofColor c;
		return c;
	};
}

Color::Color(function<ofColor()> f){
	get_ofColor = f;
}

Color::Color(Value r, Value g, Value b, Value a){
	get_ofColor = [=](){
		ofColor c(255*r(), 255*g(), 255*b(), 255*a());
		return c;
	};
}

Color make_color(string name, py::list args){

	if(name=="rgb"){
		Value r, g, b, a;

		if(py::len(args) <= 2){
			r = Value(args, 0, 1.0);
			g = Value(r);
			b = Value(r);
			a = Value(args, 1, 1.0);
		}else{
			r = Value(args, 0, 1.0);
			g = Value(args, 1, 1.0);
			b = Value(args, 2, 1.0);
			a = Value(args, 3, 1.0);
		}

		return Color(r, g, b, a);
	}

	if(name=="lerp"){
		Value amount(args, 0, 0.0);
		Color p = py::extract<Color>(args[1]);
		Color q = py::extract<Color>(args[2]);

		return Color([=](){
			ofColor c1 = p.get_ofColor();
			ofColor c2 = q.get_ofColor();

			return c1.getLerped(c2, amount());
		});
	}

	if(name=="invert"){
		Color in_color = py::extract<Color>(args[0]);

		return Color([=](){
			ofColor c = in_color.get_ofColor();
			return c.getInverted();
		});
	}

	return Color();
}
