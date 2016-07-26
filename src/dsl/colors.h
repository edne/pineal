{{ begin_module("colors") }}

	{{ module.bind("make_color", "make_color") }}
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

			return Color(ofColor(255*r(), 255*g(), 255*b(), 255*a()));
		}

		if(name=="lerp"){
			Value amount(args, 0, 0.0);
			Color p = py::extract<Color>(args[1]);
			Color q = py::extract<Color>(args[2]);

			return Color(p.c.getLerped(q.c, amount()));
		}

		if(name=="invert"){
			Color in_color = py::extract<Color>(args[0]);

			return Color(in_color.c.getInverted());
		}

		return Color();
	}

{{ end_module() }}
