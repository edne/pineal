{{ begin_module("colors") }}

	void setup(){
		ofSetColor(255);
		ofFill();
		ofSetLineWidth(1);
	}

	{{ module.bind("lerp", "lerp") }}
	Color lerp(float amount, Color p, Color q){
		return Color(p.c.getLerped(q.c, amount));
	}

	{{ module.bind("invert", "invert") }}
	Color invert(Color in_color){
		return Color(in_color.c.getInverted());
	}

	{{ module.bind("rgb_c", "rgb") }}
	Color rgb(py::list args){
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

{{ end_module() }}
